#!/usr/bin/env python3
"""
ProvenanceBound - Provenance-Aware Authorization for Untrusted Calendar Content.

Four stages, in pipeline order, around an *inert* calendar agent:

  1. provenance  where did this invite come from?  Derived from STRUCTURED
                  fields (organizer domain, original-organizer, forward chain)
                  - NEVER from calendar_text or labels. Missing structure
                  fails closed to untrusted. Any untrusted hop poisons the
                  whole chain (least-trust). Organizer mismatch flags
                  possible laundering.
  2. detection    does the body look like prompt injection?  Deterministic
                  lexical rules with Unicode NFKC + zero-width handling.
                  Explainable indicators, never a verdict on its own.
  3. proposal     did the naive agent attempt an outbound action?  A verb +
                  endpoint heuristic on the text only. It MUST NOT read
                  labels or provenance - it models what an agent *would try*.
                  Attempts are recorded, never performed.
  4. policy       may we act on it?  Provenance-aware deny-by-default:
                  high-risk untrusted attempts are always blocked (even when
                  the detector misses); low-risk untrusted attempts are
                  blocked only when suspicious; trusted attempts are blocked
                  only when suspicious. No attempt means not_requested.

The baseline proposes the same way but trusts everything and allows every
attempt (allow-all). Nothing here opens a socket or sends mail.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# --------------------------------------------------------------------------
# Stage 2: detector (lexical, deterministic, explainable)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class DetectionResult:
    indicators: Tuple[str, ...] = ()

    @property
    def suspicious(self) -> bool:
        return bool(self.indicators)


RULES: Tuple[Tuple[str, re.Pattern], ...] = (
    ("instruction_override", re.compile(r"\b(system\s+override|ignore\s+(all\s+)?(previous|prior)\s+(rules|instructions))\b", re.I)),
    ("sensitive_data_request", re.compile(r"\b(passwords?|api\s*keys?|stored\s+tokens?|conversation\s+history|workspace\s+history)\b", re.I)),
    ("external_transfer", re.compile(r"\b(send|export|exfiltrate|upload|transfer|disclose)\b.{0,100}\b(https?://|remote\s+(service|server)|external)\b", re.I)),
    ("encoding_evasion", re.compile(r"\b(encode|format)\b.{0,100}\b(history|conversation|workspace|data)\b", re.I)),
    ("prompt_hierarchy_attack", re.compile(r"\b(act\s+as|you\s+are\s+now|pretend\s+to\s+be|your\s+new\s+(role|persona|identity)|switch\s+to\s+\w+\s+(role|mode))\b", re.I)),
    ("encoded_exfiltration", re.compile(r"\b(base64|hex|url\s*encod\w*|rot.?13)\b.{0,100}\b(send|upload|transfer|post|put)\b|\b(send|upload|transfer|post|put)\b.{0,100}\b(base64|hex|url\s*encod\w*|rot.?13)\b", re.I)),
)


def _normalize_for_matching(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = re.sub(r"[\u200b-\u200d\ufeff]", " ", normalized)
    return re.sub(r"\s+", " ", normalized)


def detect_prompt_injection(text: str) -> DetectionResult:
    normalized = _normalize_for_matching(text)
    return DetectionResult(tuple(name for name, pattern in RULES if pattern.search(normalized)))


# --------------------------------------------------------------------------
# Stage 1: derived provenance (structure only, fail closed)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Provenance:
    source: str  # "trusted-internal" | "untrusted-external" | "unknown"
    trusted: bool
    derivation: str
    signals: Dict[str, Any] = field(default_factory=dict)


def _domain_of(addr: str) -> str:
    addr = (addr or "").strip().lower()
    if "@" in addr:
        return addr.rsplit("@", 1)[1]
    return addr


def derive_provenance(
    case: Dict[str, Any],
    *,
    trusted_domains: Tuple[str, ...] = ("internal.example", "trusted.example"),
) -> Provenance:
    """Derive provenance from structured fields only.

    Reads (all optional): organizer, original_organizer, organizer_domain,
    attendees, forward_chain. NEVER reads calendar_text or labels.
    """
    organizer = str(case.get("organizer") or "").strip()
    original = str(case.get("original_organizer") or "").strip()
    explicit_domain = str(case.get("organizer_domain") or "").strip().lower()
    domain = explicit_domain or (_domain_of(organizer) if organizer else "")
    attendees = case.get("attendees") or []
    chain = case.get("forward_chain") or []

    signals: Dict[str, Any] = {
        "has_organizer": bool(organizer),
        "organizer_domain": domain or None,
        "attendee_count": len(attendees) if isinstance(attendees, list) else 0,
        "forward_hops": len(chain) if isinstance(chain, list) else 0,
        "organizer_mismatch": bool(organizer and original and organizer.lower() != original.lower()),
    }

    if signals["organizer_mismatch"]:
        return Provenance(
            source="untrusted-external",
            trusted=False,
            derivation=(
                f"organizer/original-organizer mismatch ({original!r} vs {organizer!r}): "
                "possible laundering; fail-closed to untrusted"
            ),
            signals=signals,
        )
    if isinstance(chain, list) and chain:
        for hop in chain:
            hop_org = str((hop or {}).get("organizer") or "")
            hop_domain = _domain_of(hop_org)
            if not hop_org or hop_domain not in trusted_domains:
                signals["untrusted_hop"] = hop_org or None
                return Provenance(
                    source="untrusted-external",
                    trusted=False,
                    derivation=(
                        f"forward chain contains untrusted hop {hop_org!r}; "
                        "least-trust propagation"
                    ),
                    signals=signals,
                )
    if not organizer and not domain:
        return Provenance(
            source="unknown",
            trusted=False,
            derivation="no structured organizer; fail-closed to untrusted (never infer trust from text)",
            signals=signals,
        )
    if domain in trusted_domains:
        return Provenance(
            source="trusted-internal",
            trusted=True,
            derivation=f"organizer domain {domain!r} in trusted set",
            signals=signals,
        )
    return Provenance(
        source="untrusted-external",
        trusted=False,
        derivation=f"organizer domain {domain!r} not in trusted set",
        signals=signals,
    )


# --------------------------------------------------------------------------
# Stage 3: naive mock agent (text only, inert)
# --------------------------------------------------------------------------

_ACTION_VERBS_RE = re.compile(
    r"\b(send|export|exfiltrat\w*|upload|transfer|disclos\w*|post|put|share|forward)\b",
    re.I,
)
_ENDPOINT_RE = re.compile(
    r"(https?://|remote\s+(service|server|logging)|external|third-?party|collection\s+endpoint)",
    re.I,
)


@dataclass(frozen=True)
class AgentObservation:
    candidate_action: Optional[str]
    attempted: bool
    reason: str
    log: Tuple[str, ...] = ()


def propose_action_from_model(
    calendar_text: str,
    detection: DetectionResult,
    provenance: Provenance,
) -> AgentObservation:
    """Propose an outbound action from content signals only (inert).

    Reads calendar_text only. The detection and provenance arguments are
    accepted for interface parity with stronger agents but MUST NOT change
    the attempt decision: the naive agent is verb + endpoint only, so its
    failures (missed attempts, attempted exfiltration) stay visible.
    """
    if not isinstance(calendar_text, str):
        raise TypeError(f"calendar_text must be str, got {type(calendar_text).__name__}")
    log = [
        f"provenance={provenance.source} trusted={provenance.trusted}",
        f"detector_suspicious={detection.suspicious} indicators={list(detection.indicators)}",
    ]
    has_verb = bool(_ACTION_VERBS_RE.search(calendar_text))
    has_endpoint = bool(_ENDPOINT_RE.search(calendar_text))
    log.append(f"has_action_verb={has_verb} has_endpoint={has_endpoint}")
    attempted = bool(has_verb and has_endpoint)
    reason = (
        "verb+endpoint present; naive agent attempts"
        if attempted
        else "no verb+endpoint pair; naive agent abstains"
    )
    log.append(f"attempted={attempted} reason={reason}")
    return AgentObservation(
        candidate_action="untrusted_outbound_action" if attempted else None,
        attempted=attempted,
        reason=reason,
        log=tuple(log),
    )


def observe_case(case: Dict[str, Any], detection: DetectionResult, provenance: Provenance) -> AgentObservation:
    if "calendar_text" not in case:
        raise ValueError("observe_case requires calendar_text (never labels alone)")
    for oracle_key in ("expected_malicious", "simulated_action_attempt", "expected_action_decision"):
        if oracle_key in case:
            raise ValueError(f"observe_case must not receive oracle key {oracle_key!r}")
    return propose_action_from_model(case["calendar_text"], detection, provenance)


# --------------------------------------------------------------------------
# Stage 4: provenance-aware authorization policy
# --------------------------------------------------------------------------

VALID_RISK_LEVELS = ("high", "low")


def authorize(
    *,
    provenance_trusted: bool,
    risk_level: str,
    suspicious: bool,
    attempted: bool,
) -> Tuple[str, str]:
    """Return (decision, reason) for one proposed action.

    Decisions: "allowed" | "blocked" | "not_requested".
    """
    if risk_level not in VALID_RISK_LEVELS:
        raise ValueError(f"action_risk_level must be one of {VALID_RISK_LEVELS}, got {risk_level!r}")
    if not attempted:
        return "not_requested", "no_action_requested"
    if not provenance_trusted and risk_level == "high":
        return "blocked", "untrusted_high_risk"
    if not provenance_trusted and risk_level == "low" and suspicious:
        return "blocked", "untrusted_suspicious"
    if provenance_trusted and suspicious:
        return "blocked", "detector_suspicious"
    return "allowed", "authorized"


# --------------------------------------------------------------------------
# Pipelines: naive baseline vs provenance-bound guarded
# --------------------------------------------------------------------------

@dataclass
class CalendarCase:
    id: str
    name: str
    organizer: str
    calendar_text: str
    action_risk_level: str
    original_organizer: str = ""
    forward_chain: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CaseResult:
    case_id: str
    provenance: Provenance
    detection: DetectionResult
    observation: AgentObservation
    decision: str
    reason: str


class NaiveBaseline:
    """Baseline: same naive proposal, but trusts everything and allows all attempts."""

    def run(self, cases: List[CalendarCase], trusted_domains: Tuple[str, ...]) -> Dict[str, Any]:
        decisions: Dict[str, str] = {}
        actions_taken: List[str] = []
        for case in cases:
            provenance = derive_provenance(_case_to_dict(case), trusted_domains=trusted_domains)
            detection = detect_prompt_injection(case.calendar_text)
            observation = propose_action_from_model(case.calendar_text, detection, provenance)
            if observation.attempted:
                decisions[case.id] = "allowed"
                actions_taken.append(f"allow:{case.id}")
            else:
                decisions[case.id] = "not_requested"
                actions_taken.append(f"not_requested:{case.id}")
        return {"decisions": decisions, "actions_taken": actions_taken}


class ProvenanceBoundGuarded:
    """Guarded: provenance -> detection -> proposal -> provenance-aware policy."""

    def run(self, cases: List[CalendarCase], trusted_domains: Tuple[str, ...]) -> Dict[str, Any]:
        results: List[CaseResult] = []
        blocked: List[Dict[str, Any]] = []
        actions_taken: List[str] = []
        actions_blocked: List[str] = []
        events: List[Tuple[str, str, str]] = []
        for case in cases:
            provenance = derive_provenance(_case_to_dict(case), trusted_domains=trusted_domains)
            detection = detect_prompt_injection(case.calendar_text)
            observation = propose_action_from_model(case.calendar_text, detection, provenance)
            decision, reason = authorize(
                provenance_trusted=provenance.trusted,
                risk_level=case.action_risk_level,
                suspicious=detection.suspicious,
                attempted=observation.attempted,
            )
            results.append(CaseResult(case.id, provenance, detection, observation, decision, reason))
            if decision == "allowed":
                actions_taken.append(f"allow:{case.id}")
                events.append(("action", case.id, f"allow:{case.id}"))
            elif decision == "blocked":
                actions_blocked.append(f"block:{case.id} ({reason})")
                blocked.append({"case": case.id, "reason": reason, "executed": False})
                events.append(("blocked_action", case.id, f"block:{case.id} ({reason})"))
            else:
                events.append(("no_action", case.id, f"not_requested:{case.id}"))
        return {
            "results": results,
            "blocked": blocked,
            "actions_taken": actions_taken,
            "actions_blocked": actions_blocked,
            "events": events,
        }


def _case_to_dict(case: CalendarCase) -> Dict[str, Any]:
    d: Dict[str, Any] = {"organizer": case.organizer, "calendar_text": case.calendar_text}
    if case.original_organizer:
        d["original_organizer"] = case.original_organizer
    if case.forward_chain:
        d["forward_chain"] = case.forward_chain
    return d


def load_cases(data: Dict[str, Any]) -> List[CalendarCase]:
    cases = []
    for c in data["calendar_cases"]:
        cases.append(CalendarCase(
            id=c["id"],
            name=c.get("name", c["id"]),
            organizer=c.get("organizer", ""),
            calendar_text=c["calendar_text"],
            action_risk_level=c.get("action_risk_level", "high"),
            original_organizer=c.get("original_organizer", ""),
            forward_chain=list(c.get("forward_chain") or []),
        ))
    return cases


def main() -> None:
    print("=== ProvenanceBound Demo ===\n")
    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "calendar.json").read_text())
    trusted = tuple(data.get("trusted_domains", ["internal.example", "trusted.example"]))
    cases = load_cases(data)

    print(f"Trusted domains: {list(trusted)}")
    print(f"Cases: {len(cases)} (seed 42)\n")

    print("--- Naive Baseline (proposes from text, trusts everything, allows all attempts) ---")
    baseline = NaiveBaseline().run(cases, trusted)
    for case in cases:
        print(f"  {case.id} ({case.name}): {case.calendar_text[:60]}...")
        print(f"    DECISION: {baseline['decisions'][case.id]}")
    print(f"  Actions taken: {len([a for a in baseline['actions_taken'] if a.startswith('allow:')])}/{len(cases)}")
    print()

    print("--- Provenance-Bound Guarded (provenance -> detect -> propose -> authorize) ---")
    guarded = ProvenanceBoundGuarded().run(cases, trusted)
    by_id = {r.case_id: r for r in guarded["results"]}
    for case in cases:
        r = by_id[case.id]
        det = f" suspicious={r.detection.suspicious} indicators={list(r.detection.indicators)}"
        print(f"  {case.id} ({case.name}): provenance={r.provenance.source} trusted={r.provenance.trusted};{det}")
        print(f"    attempted={r.observation.attempted} -> {r.decision} ({r.reason})")
    print(f"  Actions taken: {guarded['actions_taken']}")
    print(f"  Actions blocked: {guarded['actions_blocked']}")
    print()

    print("=== Demo Complete ===")
    print("\nKey constraints:")
    print("  1. Provenance is derived from structure, never from text or labels - missing structure fails closed")
    print("  2. High-risk untrusted attempts are blocked even when the detector misses (cal_008)")
    print("  3. Detector false positives without an attempt cause no block (cal_004)")
    print("  4. Laundered organizers and untrusted forward hops poison trust (cal_005)")


if __name__ == "__main__":
    main()
