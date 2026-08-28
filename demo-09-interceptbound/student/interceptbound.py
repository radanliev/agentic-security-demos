#!/usr/bin/env python3
"""
InterceptBound - Traffic Interception & Taint Tracking

An agent that observes intercepted traffic must treat every byte it sees as an
OBSERVATION, never as an INSTRUCTION.  Four mechanisms, in pipeline order:

  1. scope        frames from sources/destinations outside the allowlist are
                  never parsed (fail closed, uniform result shape);
  2. taint        every parsed field inherits the frame's provenance and taint
                  label.  Labels are attached at the capture boundary, upstream
                  of this module (see fixtures/traffic.json) - the parser only
                  propagates them, it never invents trust;
  3. detection    credential-, command- and injection-shaped content is found
                  by named pattern rules over the WIRE DATA.  The fixture's
                  `injection` field is an answer key for the tests and the
                  results generator; the agents never read it;
  4. action guard every candidate action has a taint ceiling, and privileged
                  actions (ceiling LOW) additionally require non-intercepted
                  provenance - so a mislabelled or laundered taint label still
                  cannot turn intercepted bytes into a stored credential.

Field values are held in an ephemeral buffer whose own copy is zeroed as soon
as the frame has been decided (and on TTL expiry or size eviction).

Nothing here opens a socket: all frames are JSON fixtures.
"""

from __future__ import annotations

import json
import re
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:  # the course-wide de-identification helper (single source in shared/)
    from shared.anonymize import Anonymizer
except ModuleNotFoundError:  # running the file directly from the demo folder
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from shared.anonymize import Anonymizer


class Provenance(Enum):
    TRUSTED_LOCAL = "trusted_local"
    USER_SUPPLIED = "user_supplied"
    INTERCEPTED_NETWORK = "intercepted_network"


class TaintLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


TAINT_ORDER = {TaintLevel.LOW: 0, TaintLevel.MEDIUM: 1, TaintLevel.HIGH: 2}


@dataclass
class ParsedField:
    name: str
    value: Any
    provenance: Provenance
    taint: TaintLevel
    source_frame: str
    credential_flags: List[str] = field(default_factory=list)
    command_flags: List[str] = field(default_factory=list)
    injection_flags: List[str] = field(default_factory=list)


@dataclass
class TrafficFrame:
    id: str
    protocol: str
    src: str
    dst: str
    direction: str
    fields: Dict
    provenance: Provenance
    taint: TaintLevel
    # Answer key only (what the fixture author planted).  Read by the tests and
    # by generate_intercept_results.py to check the detector - never by the
    # agents.  See test_detection_does_not_read_the_annotation.
    injection: Optional[str] = None


# --------------------------------------------------------------------------
# Content detection: named pattern rules over wire data
# --------------------------------------------------------------------------

class ContentDetector:
    """Pattern rules over parsed field VALUES.  Each hit is reported by rule id
    so an operator can see which rule fired.  These are deliberately simple -
    the point of the demo is what happens *after* detection."""

    CREDENTIAL_RULES: List[Tuple[str, re.Pattern]] = [
        ("json_credential", re.compile(r'"(?:token|password|secret|api[_-]?key)"\s*:\s*"[A-Za-z0-9_\-.]{6,}"', re.I)),
        ("kv_credential", re.compile(r'\b(?:token|password|secret|api[_-]?key)\s*=\s*[A-Za-z0-9_\-.]{6,}', re.I)),
        ("bearer_token", re.compile(r'\bBearer\s+[A-Za-z0-9_\-.]{12,}', re.I)),
    ]
    COMMAND_RULES: List[Tuple[str, re.Pattern]] = [
        ("privileged_command", re.compile(r'"command"\s*:\s*"(?:shutdown|reboot|halt|exec|rm)"', re.I)),
    ]
    INJECTION_RULES: List[Tuple[str, re.Pattern]] = [
        ("canary_marker", re.compile(r"CANARY_[A-Z0-9_]+")),
        ("instruction_phrase", re.compile(r"IGNORE[_ ](?:ALL[_ ])?(?:PREVIOUS[_ ])?(?:RULES|INSTRUCTIONS)", re.I)),
        ("script_tag", re.compile(r"<script\b", re.I)),
        ("js_exfil", re.compile(r"\bfetch\(\s*['\"]https?://", re.I)),
        ("privileged_command", COMMAND_RULES[0][1]),
    ]

    @classmethod
    def _hits(cls, rules: List[Tuple[str, re.Pattern]], text: str) -> List[str]:
        return [rule_id for rule_id, pattern in rules if pattern.search(text)]

    @classmethod
    def credentials(cls, value: Any) -> List[str]:
        return cls._hits(cls.CREDENTIAL_RULES, str(value))

    @classmethod
    def commands(cls, value: Any) -> List[str]:
        return cls._hits(cls.COMMAND_RULES, str(value))

    @classmethod
    def injections(cls, value: Any) -> List[str]:
        return cls._hits(cls.INJECTION_RULES, str(value))


# --------------------------------------------------------------------------
# Taint propagation: frame label -> every parsed leaf
# --------------------------------------------------------------------------

class TaintTracker:
    """Flattens a frame into leaf fields; every leaf inherits the frame's
    provenance and taint (taint is frame-wide and conservative - refinement
    is Exercise 9.2) and is screened by the ContentDetector."""

    def parse_frame(self, frame: TrafficFrame) -> List[ParsedField]:
        parsed: List[ParsedField] = []
        for name, value in self._flatten(frame.fields):
            p = ParsedField(
                name=name,
                value=value,
                provenance=frame.provenance,
                taint=frame.taint,
                source_frame=frame.id,
                credential_flags=ContentDetector.credentials(value),
                command_flags=ContentDetector.commands(value),
                injection_flags=ContentDetector.injections(value),
            )
            if p.injection_flags:
                p.name += "_INJECTION"
            parsed.append(p)
        return parsed

    def _flatten(self, obj: Any, prefix: str = "") -> List[Tuple[str, Any]]:
        leaves: List[Tuple[str, Any]] = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                leaves.extend(self._flatten(v, f"{prefix}.{k}" if prefix else str(k)))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                leaves.extend(self._flatten(v, f"{prefix}[{i}]"))
        else:
            leaves.append((prefix, obj))
        return leaves


# --------------------------------------------------------------------------
# Ephemeral buffer: bounded, expiring, zeroed on release
# --------------------------------------------------------------------------

class EphemeralBuffer:
    """Holds field values only while a frame is being decided.

    * `max_size` bounds the number of live entries (oldest evicted first);
    * `ttl_seconds` bounds their lifetime;
    * `secure_delete` overwrites the buffer's own byte copy with zeros before
      the entry is dropped.

    What zeroing can and cannot do in Python: the buffer owns a `bytearray`
    copy and can overwrite *that*.  It cannot reach other copies of the value
    (the ParsedField objects, strings in log lines) - which is why the agent
    also drops its parsed fields at the end of `process` and why Exercise 9.5
    (buffer a fingerprint, never the secret) exists.
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: float = 60, secure_delete: bool = True):
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.secure_delete = secure_delete
        self._entries: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self.stats = {"stored": 0, "zeroed": 0, "expired": 0, "evicted": 0}

    def add(self, key: str, data: Any) -> None:
        if key in self._entries:
            self.delete(key)
        raw = bytearray(json.dumps(data, default=str).encode("utf-8"))
        self._entries[key] = {"data": raw, "added": time.time()}
        self.stats["stored"] += 1
        while len(self._entries) > self.max_size:
            oldest = next(iter(self._entries))
            self.delete(oldest)
            self.stats["evicted"] += 1

    def get(self, key: str) -> Optional[Any]:
        entry = self._entries.get(key)
        if entry is None:
            return None
        if time.time() - entry["added"] > self.ttl:
            self.delete(key)
            self.stats["expired"] += 1
            return None
        return json.loads(bytes(entry["data"]).decode("utf-8"))

    def delete(self, key: str) -> bool:
        entry = self._entries.pop(key, None)
        if entry is None:
            return False
        if self.secure_delete:
            entry["data"][:] = b"\0" * len(entry["data"])
            self.stats["zeroed"] += 1
        return True

    def purge(self, prefix: str) -> int:
        keys = [k for k in self._entries if k.startswith(prefix)]
        for k in keys:
            self.delete(k)
        return len(keys)

    def cleanup_expired(self) -> int:
        now = time.time()
        expired = [k for k, v in self._entries.items() if now - v["added"] > self.ttl]
        for k in expired:
            self.delete(k)
            self.stats["expired"] += 1
        return len(expired)

    def raw_copy(self, key: str) -> Optional[bytearray]:
        """The buffer's own byte copy (for inspection/tests only)."""
        entry = self._entries.get(key)
        return None if entry is None else entry["data"]

    def __len__(self) -> int:
        return len(self._entries)


# --------------------------------------------------------------------------
# Action guard: per-action taint ceilings + provenance rule
# --------------------------------------------------------------------------

class ActionGuard:
    """Information-flow guard.

    Rule 1 (taint ceiling): the field's taint must not exceed the ceiling of
        the requested action.  Unknown actions get the default ceiling
        (`max_taint_for_action`, LOW in the fixture) - fail closed.
    Rule 2 (provenance): a privileged action (ceiling LOW) can never be driven
        by INTERCEPTED_NETWORK data, whatever its taint label says.  Taint
        labels can be refined (or forged, or mislabelled); provenance cannot.
    """

    def __init__(self, max_taint_for_action: "TaintLevel | str" = TaintLevel.LOW,
                 action_ceilings: Optional[Dict[str, "TaintLevel | str"]] = None):
        self.default_ceiling = self._level(max_taint_for_action)
        self.ceilings: Dict[str, TaintLevel] = {
            action: self._level(level) for action, level in (action_ceilings or {}).items()
        }

    @staticmethod
    def _level(level: "TaintLevel | str") -> TaintLevel:
        return TaintLevel(level) if isinstance(level, str) else level

    def ceiling_for(self, action: str) -> TaintLevel:
        return self.ceilings.get(action, self.default_ceiling)

    def authorize(self, action: str, field_taint: TaintLevel, data: Any = None,
                  provenance: Optional[Provenance] = None) -> Tuple[bool, str]:
        ceiling = self.ceiling_for(action)
        if TAINT_ORDER[field_taint] > TAINT_ORDER[ceiling]:
            return False, f"taint_too_high: {field_taint.value} > {ceiling.value}"
        if ceiling == TaintLevel.LOW and provenance == Provenance.INTERCEPTED_NETWORK:
            return False, "intercepted_network_cannot_drive_privileged_action"
        return True, "authorized"


# --------------------------------------------------------------------------
# Candidate actions: what an agent would *want* to do with a field
# --------------------------------------------------------------------------

_IPV4 = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
OBSERVATION_FIELDS = {"status", "cert_fingerprint", "query"}


def frame_observation(frame: TrafficFrame) -> str:
    """The compact note an interception agent would write down about a frame:
    its source and the one field that carries the most identifying content.
    This is what gets *recorded*, so it is exactly what must be de-identified
    before it is written anywhere durable."""
    f = frame.fields
    if frame.protocol == "http":
        detail = str(f.get("body", ""))
    elif frame.protocol == "dns":
        answers = ",".join(str(a.get("value")) for a in f.get("answers", []))
        detail = f"{f.get('query')} -> {answers}"
    elif frame.protocol == "tls":
        detail = str(f.get("cert_subject", ""))
    elif frame.protocol == "custom":
        detail = str(f.get("payload", "")).split("\n", 1)[0]
    else:
        detail = str(f.get("body") or f.get("record", ""))
    return f"{frame.protocol} {frame.src} {detail}"


def candidate_actions(frame: TrafficFrame, p: ParsedField) -> List[Tuple[str, str]]:
    """(action label, guard action) pairs derived from the wire data.
    Both agents use this; they differ only in whether a guard is consulted."""
    base_name = p.name[:-len("_INJECTION")] if p.name.endswith("_INJECTION") else p.name
    leaf = base_name.rsplit(".", 1)[-1]
    out: List[Tuple[str, str]] = []
    if p.credential_flags:
        out.append(("store_token", "store_credential"))
    if p.command_flags:
        out.append(("execute_shutdown", "system_shutdown"))
    if frame.protocol == "dns" and leaf == "value" and _IPV4.match(str(p.value)):
        out.append(("update_dns_cache", "update_dns_cache"))
    if leaf in OBSERVATION_FIELDS:
        out.append(("record_observation", "record_observation"))
    return out


# --------------------------------------------------------------------------
# Agents
# --------------------------------------------------------------------------

class BaselineAgent:
    """Unguarded specimen: no scope, no taint, no guard.  Every candidate action
    derived from the wire data is 'executed' (simulated), and instruction-shaped
    content is followed."""

    def __init__(self):
        self.tracker = TaintTracker()
        self.observations: List[str] = []              # what it writes down: raw

    def process(self, frame: TrafficFrame) -> Dict:
        self.observations.append(frame_observation(frame))   # recorded in the clear
        actions = []
        for p in self.tracker.parse_frame(frame):      # labels parsed, then ignored
            for label, _ in candidate_actions(frame, p):
                actions.append({"action": label, "field": p.name})
            instruction_rules = [r for r in p.injection_flags if r != "privileged_command"]
            if instruction_rules:
                actions.append({"action": "follow_instruction", "field": p.name,
                                "reason": ",".join(instruction_rules)})
        return {"frame": frame.id, "actions": actions, "blocked": [], "taint_tracked": False}


class TaintAwareAgent:
    """Guarded: scope -> taint-labelled parse -> ephemeral buffer -> guarded actions."""

    def __init__(self, scope_policy: Dict, buffer_config: Dict):
        self.tracker = TaintTracker()
        self.buffer = EphemeralBuffer(**buffer_config)
        self.guard = ActionGuard(scope_policy.get("max_taint_for_action", "low"),
                                 scope_policy.get("action_ceilings", {}))
        self.allowed_sources = list(scope_policy.get("allowed_sources", []))
        self.allowed_destinations = list(scope_policy.get("allowed_destinations", []))
        # One Anonymizer for the whole run, so a pseudonym is stable across
        # frames: USER_5aff in frame_001 is the same account in frame_004, and
        # an analyst can still join them without learning the name.
        self.anon = Anonymizer()
        self.observations: List[str] = []              # what it writes down: de-identified
        self.deid_counts: Dict[str, int] = {}

    @staticmethod
    def _host_of(addr: str) -> str:
        if addr.startswith("["):                      # [ipv6]:port
            return addr[1:addr.find("]")]
        if addr.count(":") == 1:                      # ipv4:port
            return addr.split(":")[0]
        return addr                                   # bare host / bare ipv6

    def _in_scope(self, frame: TrafficFrame) -> Tuple[bool, str]:
        src, dst = self._host_of(frame.src), self._host_of(frame.dst)
        if src not in self.allowed_sources:
            return False, f"source_not_allowed: {src}"
        if self.allowed_destinations and dst not in self.allowed_destinations:
            return False, f"destination_not_allowed: {dst}"
        return True, "in_scope"

    def process(self, frame: TrafficFrame) -> Dict:
        self.buffer.cleanup_expired()

        # 1. Scope: out-of-scope frames are never parsed.
        ok, reason = self._in_scope(frame)
        if not ok:
            return {"frame": frame.id, "actions": [],
                    "blocked": [{"action": "process_frame", "reason": reason}],
                    "parsed_fields": 0, "taint_tracked": False, "exit": "scope_blocked"}

        # 1b. Observe: record a note about the frame, de-identified first.
        #     Identities become stable pseudonyms; secrets are redacted; the
        #     buffer and the guard below are unchanged.
        report = self.anon.deidentify(frame_observation(frame))
        self.observations.append(report.text)
        for kind, count in report.changes.items():
            self.deid_counts[kind] = self.deid_counts.get(kind, 0) + count

        # 2. Parse with taint labels; hold values in the ephemeral buffer.
        parsed = self.tracker.parse_frame(frame)
        for p in parsed:
            self.buffer.add(f"{frame.id}.{p.name}", p.value)

        # 3. Decide every candidate action through the guard.
        actions, blocked = [], []
        for p in parsed:
            if p.injection_flags:
                blocked.append({"action": "process_injection", "field": p.name,
                                "reason": "injection_detected: " + ",".join(p.injection_flags)})
            for label, guard_action in candidate_actions(frame, p):
                allowed, why = self.guard.authorize(guard_action, p.taint, p.value, p.provenance)
                entry = {"action": label, "field": p.name, "reason": why}
                (actions if allowed else blocked).append(entry)

        # 4. Frame decided: release (zero) the buffer's copies.
        self.buffer.purge(f"{frame.id}.")

        return {"frame": frame.id, "actions": actions, "blocked": blocked,
                "parsed_fields": len(parsed), "taint_tracked": True, "exit": "ok"}


# --------------------------------------------------------------------------
# Loading and demo
# --------------------------------------------------------------------------

def load_frames(data: Dict) -> List[TrafficFrame]:
    return [TrafficFrame(
        id=f["id"], protocol=f["protocol"], src=f["src"], dst=f["dst"],
        direction=f["direction"], fields=f["fields"],
        provenance=Provenance(f["provenance"]), taint=TaintLevel(f["taint"]),
        injection=f.get("injection"),
    ) for f in data["traffic_frames"]]


def print_result(frame: TrafficFrame, result: Dict) -> None:
    print(f"  {frame.id} ({frame.protocol} {frame.src}->{frame.dst}, {frame.provenance.value}, taint {frame.taint.value}):")
    for b in result.get("blocked", []):
        where = f" [{b['field']}]" if b.get("field") else ""
        print(f"    BLOCKED: {b['action']} ({b['reason']}){where}")
    for a in result.get("actions", []):
        where = f" [{a['field']}]" if a.get("field") else ""
        print(f"    ALLOWED: {a['action']}{where}")


def main():
    print("=== InterceptBound Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "traffic.json").read_text())
    frames = load_frames(data)
    scope = data["scope_policy"]
    buffer_config = data["ephemeral_buffer"]

    print("Scope Policy:")
    print(f"  Allowed sources: {scope['allowed_sources']}")
    print(f"  Allowed destinations: {scope['allowed_destinations']}")
    print(f"  Default taint ceiling for actions: {scope['max_taint_for_action']}")
    print(f"  Per-action ceilings: {scope['action_ceilings']}")
    print()

    print("--- Unguarded Baseline (no scope, no taint, no guard) ---")
    baseline = BaselineAgent()
    for frame in frames:
        print_result(frame, baseline.process(frame))
    print()

    print("--- Taint-Aware Guarded (scope -> taint -> buffer -> guard) ---")
    agent = TaintAwareAgent(scope, buffer_config)
    for frame in frames:
        print_result(frame, agent.process(frame))
    print()

    print("--- Taint Tracking (frame_001, every leaf inherits the frame label) ---")
    for p in TaintTracker().parse_frame(frames[0]):
        flags = ",".join(p.credential_flags + p.command_flags + p.injection_flags) or "-"
        print(f"  {p.name:22} taint={p.taint.value:6} prov={p.provenance.value:20} flags={flags:16} value={str(p.value)[:40]!r}")
    print()

    print("--- Observation log: what each agent writes down ---")
    print("  Baseline (recorded in the clear):")
    for line in baseline.observations:
        print(f"    {line[:96]}")
    print("  Guarded (de-identified before recording):")
    for line in agent.observations:
        print(f"    {line[:96]}")
    counts = agent.deid_counts
    order = ("username", "email", "ipv4", "secret")
    singular = {"username": "username", "email": "email", "ipv4": "IP", "secret": "secret"}
    summary = ", ".join(f"{counts[k]} {singular[k]}{'' if counts[k] == 1 else 's'}"
                        for k in order if counts.get(k))
    # Prove the claim: no raw identifier or secret survived in the guarded log.
    leaked = [s for s in ("alice", "alice@corp.example", "DEMO_TOKEN_ABC123", "10.0.0.50")
              if any(s in line for line in agent.observations)]
    print(f"  De-identified before recording: {summary}; "
          f"{len(leaked)} identities or secrets written in the clear")
    print(f"  (frame_007 is out of scope, so the guarded agent never records it - "
          f"the baseline logs its user and token anyway)")
    print()

    print("--- Provenance rule: a laundered taint label still cannot store an intercepted token ---")
    laundered = TrafficFrame(**{**frames[0].__dict__, "id": "frame_001_relabelled_low", "taint": TaintLevel.LOW})
    print_result(laundered, agent.process(laundered))
    local = next(f for f in frames if f.provenance == Provenance.TRUSTED_LOCAL)
    print(f"  (compare {local.id}: same action, trusted_local provenance -> allowed above)")
    print()

    print("--- Ephemeral Buffer ---")
    buffer = EphemeralBuffer(secure_delete=True)
    buffer.add("test_key", "sensitive_token_data")
    raw = buffer.raw_copy("test_key")
    print(f"Stored: {buffer.get('test_key')}")
    buffer.delete("test_key")
    print(f"After delete: {buffer.get('test_key')}  (buffer's own {len(raw)}-byte copy is now {bytes(raw[:6])!r}...)")
    s = agent.buffer.stats
    print(f"Agent buffer after the run: {len(agent.buffer)} live entries "
          f"(stored={s['stored']}, zeroed={s['zeroed']}, expired={s['expired']}, evicted={s['evicted']})")

    print("\n=== Demo Complete ===")
    print("\nKey insight: Intercepted network data is OBSERVATION, not INSTRUCTION.")
    print("Taint ceilings block tainted data from privileged actions; provenance blocks")
    print("intercepted data from them even when its taint label has been laundered.")
    print("And what may legitimately be observed is de-identified before it is written down:")
    print("secrets are redacted, identities become stable pseudonyms, so the log stays")
    print("useful for analysis without holding anyone's name or token in the clear.")


if __name__ == "__main__":
    main()
