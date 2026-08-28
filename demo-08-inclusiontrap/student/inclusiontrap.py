#!/usr/bin/env python3
"""
InclusionTrap - File Inclusion & Scope Boundaries

Everything runs against a SIMULATED host: the "filesystem" is a dict, the "remote server" is a
dict of canned responses, and every capability an agent uses goes through `Host`, which records
the call. Nothing is opened on the real disk, nothing is sent on the network, and a recorded
`exec(...)` is exactly that - a record of what the vulnerable agent *asked for*, never performed.

The thesis: READING content grants that content no authority. The guarded agent's only calls
are `read_file`/`fetch_url`, it checks scope BEFORE it reads, and content that looks like an
instruction is held as data and never turned into a call.
"""

import json
import posixpath
import re
import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:  # the course-wide de-identification helper (single source in shared/)
    from shared.anonymize import Anonymizer
except ModuleNotFoundError:  # running the file directly from the demo folder
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from shared.anonymize import Anonymizer


class Provenance(Enum):
    FILE_SYSTEM = "file_system"
    SIMULATED_REMOTE = "simulated_remote"


@dataclass
class InclusionResult:
    scenario_id: str
    included_content: str        # first 120 chars, only when the read was allowed; "" otherwise (no leak)
    provenance: Provenance
    action: str                  # "allowed" | "blocked" | "executed"
    reason: str
    host_calls: List[str] = field(default_factory=list)   # what the agent asked the host to do
    deidentified: Dict[str, int] = field(default_factory=dict)   # what the guard scrubbed before logging


# Instruction-shaped content, and the privileged action a naive interpreter would turn it into.
INSTRUCTION_PATTERNS: List[Tuple[str, Optional[str]]] = [
    (r"ignore[\s_]+(?:your[\s_]+|all[\s_]+)?previous[\s_]+instructions?", None),   # steering, no action by itself
    (r"system[\s_]+override", None),
    (r"send[\s_]+all[\s_]+logs[\s_]+to[\s_]+\w+", "network_request"),
    (r"rm\s+-rf\s+\S+", "exec"),
    (r"exec\s*\([^)]*\)", "exec"),
    (r"eval\s*\([^)]*\)", "exec"),
    (r"subprocess\.\w+\([^)]*\)", "exec"),
    (r"write[\s_]+file[\s_]+\S+", "write_file"),
]


class InjectionDetector:
    """Detect instruction-shaped content in included data. Returns the matched text (what was seen)."""

    def detect(self, content: str) -> List[str]:
        hits = []
        for pattern, _ in INSTRUCTION_PATTERNS:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                hits.append(m.group(0))
        return hits

    def instructions(self, content: str) -> List[Tuple[str, str]]:
        """(action, text) pairs a naive interpreter would execute. Only the vulnerable agent calls this."""
        found = []
        for pattern, action in INSTRUCTION_PATTERNS:
            if action is None:
                continue
            for m in re.finditer(pattern, content, re.IGNORECASE):
                found.append((action, m.group(0)))
        return found


class Host:
    """The simulated machine. Every capability call is recorded; none has a side effect."""

    def __init__(self, files: Dict[str, str], remote: Dict[str, str], denied_actions: List[str]):
        self.files = dict(files)
        self.remote = dict(remote)
        self.denied_actions = set(denied_actions)
        self.calls: List[Tuple[str, str]] = []

    def read_file(self, path: str) -> Optional[str]:
        self.calls.append(("read_file", path))
        return self.files.get(path)

    def fetch_url(self, url: str) -> Optional[str]:
        """Simulated remote fetch: a dict lookup. No socket is ever opened."""
        self.calls.append(("fetch_url", url))
        return self.remote.get(url)

    def act(self, action: str, argument: str) -> str:
        """A privileged action requested BY CONTENT. Recorded only - nothing is run, written or sent."""
        self.calls.append((action, argument))
        return f"{action}({argument!r})"

    def counts(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for action, _ in self.calls:
            out[action] = out.get(action, 0) + 1
        return out

    def privileged_calls(self) -> List[Tuple[str, str]]:
        return [c for c in self.calls if c[0] in self.denied_actions]


class ScopePolicy:
    """Read scope: allow/deny prefix globs over CANONICAL absolute paths, plus an include-URL allowlist."""

    def __init__(self, allowed: List[str], denied: List[str], allowed_urls: Optional[List[str]] = None):
        self.allowed = list(allowed)
        self.denied = list(denied)
        self.allowed_urls = list(allowed_urls or [])

    @staticmethod
    def _match(pattern: str, path: str) -> bool:
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return path.startswith(prefix)   # "/app/config/*" -> "/app/config/" : the slash keeps /app/configuration out
        return pattern == path

    def can_read(self, path: str) -> bool:
        """Deny wins; the path must be absolute and canonical (no '.', '..' or empty segments)."""
        if not path.startswith("/") or posixpath.normpath(path) != path or "\\" in path:
            return False
        if any(seg in ("..", ".") for seg in path.split("/")):
            return False
        if any(self._match(p, path) for p in self.denied):
            return False
        return any(self._match(p, path) for p in self.allowed)

    def can_include_url(self, url: str) -> bool:
        return any(self._match(p, url) for p in self.allowed_urls)

    def explain(self, path: str) -> str:
        if not path.startswith("/") or posixpath.normpath(path) != path or "\\" in path \
                or any(seg in ("..", ".") for seg in path.split("/")):
            return f"{path!r} is not a canonical absolute path"
        for p in self.denied:
            if self._match(p, path):
                return f"{path} matches denied pattern {p}"
        return f"{path} not in allowed paths"


def extract_target(request: str) -> Tuple[str, str]:
    """('file', value) or ('url', value) from 'GET /view?file=...' - the web layer decodes the query once."""
    target = request.split(" ", 1)[1] if " " in request else request
    query = urllib.parse.parse_qs(urllib.parse.urlsplit(target).query, keep_blank_values=True)
    if query.get("url"):
        return "url", query["url"][0]
    if query.get("file"):
        return "file", query["file"][0]
    return "file", ""


def is_url(value: str) -> bool:
    return urllib.parse.urlsplit(value).scheme in ("http", "https")


class VulnerableInclusionAgent:
    """Vulnerable: resolves whatever it is given, reads it, and turns instruction-shaped content into calls."""

    def __init__(self, host, scope: ScopePolicy):
        self.host = host if isinstance(host, Host) else Host(host, {}, [])   # a plain files dict is accepted
        self.scope = scope          # held, never consulted
        self.detector = InjectionDetector()

    def process(self, scenario: Dict) -> InclusionResult:
        kind, target = extract_target(scenario["request"])
        before = len(self.host.calls)
        if kind == "url" or is_url(target):
            content = self.host.fetch_url(target)
            provenance = Provenance.SIMULATED_REMOTE
        else:
            content = self.host.read_file(self._resolve_path(target))
            provenance = Provenance.FILE_SYSTEM
        content = content or ""

        # VULNERABLE: detects the injection, then interprets the content anyway.
        hits = self.detector.detect(content)
        for action, text in self.detector.instructions(content):
            self.host.act(action, text)          # the vulnerability: content became a call
        calls = [f"{a}({b!r})" for a, b in self.host.calls[before:]]
        if hits:
            return InclusionResult(scenario["id"], content[:120], provenance, "executed",
                                   f"injection_detected_but_executed: {hits}", calls)
        return InclusionResult(scenario["id"], content[:120], provenance, "allowed", "no_injection", calls)

    def _resolve_path(self, path: str) -> str:
        """'Helpful' resolution: decodes and normalises traversal so the file is found (vulnerable)."""
        decoded = urllib.parse.unquote(path)
        if not decoded.startswith("/"):
            decoded = "/app/" + decoded
        return posixpath.normpath(decoded)


class GuardedInclusionAgent:
    """Guarded: canonical path, scope BEFORE read, content screened and held as data, never interpreted."""

    def __init__(self, host, scope: ScopePolicy):
        self.host = host if isinstance(host, Host) else Host(host, {}, [])   # a plain files dict is accepted
        self.scope = scope
        self.detector = InjectionDetector()
        # One Anonymizer for the run: the same account keeps the same pseudonym
        # across files, so records still join after de-identification.
        self.anon = Anonymizer()

    def process(self, scenario: Dict) -> InclusionResult:
        kind, target = extract_target(scenario["request"])
        before = len(self.host.calls)

        def result(action: str, reason: str, provenance: Provenance, content: Optional[str] = None) -> InclusionResult:
            calls = [f"{a}({b!r})" for a, b in self.host.calls[before:]]
            deid: Dict[str, int] = {}
            if action == "allowed" and content:
                # Read-only content that will be logged is DATA that may carry
                # PII: de-identify it before anything durable sees it.
                report = self.anon.deidentify(content)
                content, deid = report.text, report.changes
            shown = (content or "")[:120] if action == "allowed" else ""   # a blocked result never carries content
            return InclusionResult(scenario["id"], shown, provenance, action, reason, calls, deid)

        if kind == "url" or is_url(target):
            provenance = Provenance.SIMULATED_REMOTE
            if not self.scope.can_include_url(target):
                return result("blocked", f"scope_violation: {target} not in allowed include URLs (nothing fetched)", provenance)
            content = self.host.fetch_url(target)
        else:
            provenance = Provenance.FILE_SYSTEM
            resolved = self._resolve_path(target)
            # 1. Scope is decided on the canonical path BEFORE anything is read.
            if resolved is None:
                return result("blocked", f"scope_violation: traversal in {target!r} rejected before any read", provenance)
            if not self.scope.can_read(resolved):
                return result("blocked", f"scope_violation: {self.scope.explain(resolved)} (nothing read)", provenance)
            content = self.host.read_file(resolved)

        if content is None:
            return result("blocked", "not_found (fail closed: no fallback content)", provenance)

        # 2. Included content is DATA. Instruction-shaped data is held, never interpreted.
        hits = self.detector.detect(content)
        if hits:
            return result("blocked", f"injection_detected: {hits} (content held as data, no instruction followed)",
                          provenance, content)

        # 3. Read-only: the content is returned, and no other capability is ever called.
        return result("allowed", "safe_content_read_only", provenance, content)

    def _resolve_path(self, path: str) -> Optional[str]:
        """Canonical absolute path, or None if the request contains any traversal segment."""
        decoded = urllib.parse.unquote(path)
        segments = re.split(r"[\\/]+", decoded)
        if ".." in segments or "\\" in decoded:
            return None
        if not decoded.startswith("/"):
            decoded = posixpath.join("/app", decoded)
        return posixpath.normpath(decoded)


def build(data: Dict) -> Tuple[Host, ScopePolicy]:
    scope_cfg = data["agent_scope"]
    host = Host(data["files"], data.get("remote", {}), scope_cfg["denied_actions"])
    scope = ScopePolicy(scope_cfg["allowed_read_paths"], scope_cfg["denied_read_paths"],
                        scope_cfg.get("allowed_include_urls", []))
    return host, scope


def main():
    print("=== InclusionTrap Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "inclusion.json").read_text())
    scenarios = data["inclusion_scenarios"]
    cfg = data["agent_scope"]

    print("Agent Scope:")
    print(f"  Allowed read paths:   {cfg['allowed_read_paths']}")
    print(f"  Denied read paths:    {cfg['denied_read_paths']}")
    print(f"  Allowed include URLs: {cfg['allowed_include_urls']}")
    print(f"  Allowed actions: {cfg['allowed_actions']}   Denied actions: {cfg['denied_actions']}")
    print("  Host is simulated: files and remote responses are dict lookups; privileged calls are recorded, never run.")
    print()

    for agent_name, cls in [("Vulnerable Baseline", VulnerableInclusionAgent),
                            ("Guarded (Scope + Provenance)", GuardedInclusionAgent)]:
        print(f"--- {agent_name} ---")
        host, scope = build(data)
        agent = cls(host, scope)
        deid_total: Dict[str, int] = {}
        for scenario in scenarios:
            result = agent.process(scenario)
            safe = scenario["expected"]["safe"]
            if result.action == safe:
                status = "✓"
            elif result.action == "executed":
                status = "✗ VULNERABLE"
            else:
                status = f"✗ LEAK ({result.action}, should be {safe})"
            print(f"  {scenario['id']}: {status}")
            print(f"    Action: {result.action} ({result.reason}) [{result.provenance.value}]")
            if result.action == "allowed" and result.included_content:
                tag = "de-identified" if result.deidentified else "raw"
                print(f"    content ({tag}): {result.included_content}")
                for k, v in result.deidentified.items():
                    deid_total[k] = deid_total.get(k, 0) + v
            for call in result.host_calls:
                privileged = call.split("(")[0] in host.denied_actions
                print(f"    {'⚠️  host call' if privileged else 'host call'}: {call}"
                      + ("  [SIMULATED - recorded, not run]" if privileged else ""))
        counts = host.counts()
        summary = ", ".join(f"{a} x{counts.get(a, 0)}" for a in ["read_file", "fetch_url", "exec", "network_request", "write_file"])
        print(f"  Host call log: {summary}")
        if deid_total:
            sing = {"username": "user", "email": "email", "ipv4": "IP", "secret": "secret"}
            line = ", ".join(f"{deid_total[k]} {sing[k]}{'' if deid_total[k] == 1 else 's'}"
                             for k in ("username", "email", "ipv4", "secret") if deid_total.get(k))
            print(f"  De-identified before logging: {line} across the reads it was allowed to keep")
        print()

    print("=== Demo Complete ===")
    print("\nKey lesson: READING content ≠ GRANTING authority.")
    print("Included files are DATA. Only explicit, verified INSTRUCTIONS drive actions.")
    print("And data the guard is allowed to keep is de-identified before it is logged:")
    print("the vulnerable agent leaks /etc/passwd and the raw user list; the guarded agent")
    print("reads the same user list but records stable pseudonyms, so the ids still join.")


if __name__ == "__main__":
    main()
