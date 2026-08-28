#!/usr/bin/env python3
"""
TriageTrap - Safe Malware Triage with Provenance Tracking

Everything here is inert JSON: no sample is ever opened, decoded or run.
The score is a Bayesian posterior computed from STRUCTURED evidence only
(a sandbox verdict, accepted only when the record's provenance is a sandbox).
Free text in the record (the "canary") is an OBSERVATION: it is logged, and it
may add scrutiny (hold a record for an analyst), but it can never move the
score and never release a record.
"""

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

try:  # the course-wide de-identification helper (single source in shared/)
    from shared.anonymize import redact_record
except ModuleNotFoundError:  # running the file directly from the demo folder
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from shared.anonymize import redact_record

# When a triage record is shared, only these analytic fields go in the clear.
# Deny-by-default: any other metadata key (submitter, owner, file_name, IPs, a
# field a class has never seen) is masked, so the decision and its hashes travel
# without the identities.  This mirrors the RAID triage proxy's VirusTotal
# allowlist.
SHAREABLE_METADATA = [
    "file_hash", "sample_hash", "verdict", "score", "protocol", "mime_type",
    "src_port", "dst_port", "packet_count", "behaviors", "size",
]


class Provenance(Enum):
    TRUSTED_SENSOR = "trusted_sensor"        # network tap / endpoint sensor: observations, no verdicts
    TRUSTED_SANDBOX = "trusted_sandbox"      # detonation sandbox: the only source of a 'verdict'
    UNTRUSTED_METADATA = "untrusted_metadata"  # anything else (e-mail headers, file names, user notes)


class Verdict(Enum):
    BENIGN = "benign"           # release
    SUSPICIOUS = "suspicious"   # hold for an analyst: evidence is inconsistent or unusable
    QUARANTINE = "quarantine"   # isolate the record (a JSON verdict - nothing is moved or executed)


SANDBOX_VERDICTS = ("malicious", "benign")


@dataclass
class Artifact:
    id: str
    type: str
    source: str
    provenance: Provenance
    metadata: Dict
    canary: str


@dataclass
class TriageResult:
    artifact_id: str
    verdict: Verdict
    score: float
    reasons: List[str]
    provenance_chain: List[str]
    shared_metadata: Dict = field(default_factory=dict)   # what a shared record would carry
    redacted_fields: List[str] = field(default_factory=list)


def _share_metadata(metadata: Dict, redact: bool):
    """The metadata a triage record would expose when shared.  The guarded agent
    allowlists it (analytic fields only); the baseline shares it in the clear."""
    if redact:
        return redact_record(metadata, allow=SHAREABLE_METADATA)
    return dict(metadata), []


class BaseRateCalculator:
    """P(malicious) from a sandbox verdict, by Bayes' theorem, with the fixture's base rates."""

    REQUIRED = ("malicious_prior", "sensor_false_positive", "sandbox_false_negative", "sandbox_false_positive")

    def __init__(self, base_rates: Dict):
        missing = [k for k in self.REQUIRED if k not in base_rates]
        if missing:
            raise KeyError(f"base_rates is missing {missing}; no silent defaults for error rates")
        self.prior_malicious = float(base_rates["malicious_prior"])
        self.sensor_fp = float(base_rates["sensor_false_positive"])      # P(sensor flags | clean)
        self.sandbox_fn = float(base_rates["sandbox_false_negative"])    # P(sandbox says benign | malicious)
        self.sandbox_fp = float(base_rates["sandbox_false_positive"])    # P(sandbox says malicious | clean)

    @staticmethod
    def bayes(prior: float, p_e_given_m: float, p_e_given_not_m: float) -> float:
        """P(M | E) = P(E | M) P(M) / [ P(E | M) P(M) + P(E | not M) P(not M) ]."""
        numerator = p_e_given_m * prior
        denominator = numerator + p_e_given_not_m * (1.0 - prior)
        return numerator / denominator if denominator > 0 else 0.0

    def calculate_posterior(self, verdict: str) -> float:
        """Posterior P(malicious | sandbox verdict), using the SANDBOX's own error rates."""
        if verdict == "malicious":
            # P(says malicious | malicious) = sensitivity = 1 - FN ; P(says malicious | clean) = FP
            return self.bayes(self.prior_malicious, 1.0 - self.sandbox_fn, self.sandbox_fp)
        if verdict == "benign":
            # P(says benign | malicious) = FN ; P(says benign | clean) = specificity = 1 - FP
            return self.bayes(self.prior_malicious, self.sandbox_fn, 1.0 - self.sandbox_fp)
        raise ValueError(f"unknown sandbox verdict {verdict!r}; expected one of {SANDBOX_VERDICTS}")

    def sensor_flag_posterior(self) -> float:
        """What a single SENSOR flag would be worth (sensitivity taken from the sandbox, FP from the sensor).
        Used only for the base-rate illustration in the run header."""
        return self.bayes(self.prior_malicious, 1.0 - self.sandbox_fn, self.sensor_fp)

    def score(self, evidence: Dict) -> float:
        """Score from STRUCTURED evidence only: the sandbox verdict if there is one, else the prior."""
        verdict = evidence.get("sandbox_verdict")
        if verdict is None:
            return self.prior_malicious
        return self.calculate_posterior(verdict)


class PromptInjectionDetector:
    """Detect prompt-like payloads in free text (metadata notes, canaries)."""

    INJECTION_PATTERNS = [
        r"ignore[\s_]+(all[\s_]+)?previous[\s_]+instructions?",
        r"(?<![a-z])system[\s_]+override",
        r"disable[\s_]+(all[\s_]+)?safeguards?",
        r"quarantine[\s_]+(all|everything)\b",
        r"(?<![a-z])trust[\s_]+me(?![a-z])",
        r"definitely[\s_]+(a[\s_]+)?malware",
    ]

    def detect(self, text: str) -> List[str]:
        """Return the matched fragments (not the patterns) so a log line shows what was actually seen."""
        hits = []
        for pattern in self.INJECTION_PATTERNS:
            m = re.search(pattern, text, re.IGNORECASE)
            if m:
                hits.append(m.group(0))
        return hits


# A note that ASSERTS a label ("this is definitely malware", "confirmed benign"). Used two ways:
# the baseline believes it; the provenance-aware agent only checks it against the structured verdict.
_CLAIM_RE = re.compile(
    r"(?:this[\s_]+is|definitely|confirmed|verdict)[\s_]*(?:a[\s_]+)?(malware|malicious|benign|clean|harmless)",
    re.IGNORECASE,
)


def claimed_label(text: str) -> Optional[str]:
    m = _CLAIM_RE.search(text)
    if not m:
        return None
    return "malicious" if m.group(1).lower() in ("malware", "malicious") else "benign"


def _decide(score: float, threshold: float, hold: bool) -> Verdict:
    """Quarantine on the score; otherwise hold if the evidence was inconsistent; otherwise release."""
    if score >= threshold:
        return Verdict.QUARANTINE
    return Verdict.SUSPICIOUS if hold else Verdict.BENIGN


class BaselineTriageAgent:
    """Baseline: every string it sees is evidence, and a 'verdict' field is believed wherever it came from."""

    INJECTION_FLOOR = 0.8  # "an injection pattern is a strong malicious signal" - text moves the score

    def __init__(self, base_rates: Dict, threshold: float):
        self.calculator = BaseRateCalculator(base_rates)
        self.detector = PromptInjectionDetector()
        self.threshold = threshold

    def triage(self, artifact: Artifact) -> TriageResult:
        reasons: List[str] = []
        evidence: Dict = {}

        # No provenance check: a 'verdict' field is trusted from any record.
        verdict_field = artifact.metadata.get("verdict")
        if verdict_field in SANDBOX_VERDICTS:
            evidence["sandbox_verdict"] = verdict_field

        # Trap 2: the note overrides the structured verdict.
        claim = claimed_label(artifact.canary)
        if claim is not None:
            evidence["sandbox_verdict"] = claim
            reasons.append(f"canary claims '{claim}' -> used as the verdict")

        score = self.calculator.score(evidence)

        # Trap 1: an injection pattern is treated as evidence of maliciousness.
        injections = self.detector.detect(artifact.canary)
        if injections:
            score = max(score, self.INJECTION_FLOOR)
            reasons.append(f"prompt_injection: {injections} -> score floored at {self.INJECTION_FLOOR}")

        verdict = Verdict.QUARANTINE if score >= self.threshold else Verdict.BENIGN
        shared, redacted = _share_metadata(artifact.metadata, redact=False)  # baseline shares it all
        return TriageResult(
            artifact_id=artifact.id,
            verdict=verdict,
            score=score,
            reasons=reasons,
            provenance_chain=[artifact.provenance.value, "canary text used as evidence", f"score {score:.3f}"],
            shared_metadata=shared,
            redacted_fields=redacted,
        )


class ProvenanceAwareTriageAgent:
    """Provenance-aware: the score comes from structured evidence with sandbox provenance; text is observation."""

    def __init__(self, base_rates: Dict, threshold: float):
        self.calculator = BaseRateCalculator(base_rates)
        self.detector = PromptInjectionDetector()
        self.threshold = threshold

    def triage(self, artifact: Artifact) -> TriageResult:
        reasons: List[str] = []
        chain: List[str] = [f"{artifact.provenance.value}:{artifact.type}"]
        evidence: Dict = {}
        hold = False

        # 1. Structured evidence, gated on provenance: only a sandbox may supply a verdict.
        verdict_field = artifact.metadata.get("verdict")
        if verdict_field is not None:
            if artifact.provenance is not Provenance.TRUSTED_SANDBOX:
                reasons.append(
                    f"'verdict' field ignored: provenance {artifact.provenance.value} is not a sandbox (logged only)"
                )
            elif verdict_field in SANDBOX_VERDICTS:
                evidence["sandbox_verdict"] = verdict_field
                chain.append(f"sandbox_verdict={verdict_field}")
            else:
                hold = True  # fail closed: an unusable verdict is not evidence of anything
                reasons.append(f"unrecognised sandbox verdict {verdict_field!r}: no evidence, held for review")

        score = self.calculator.score(evidence)
        chain.append(f"bayes:P(malicious)={score:.3f}")

        # 2. Free text is an OBSERVATION. It is logged. It never touches the score.
        injections = self.detector.detect(artifact.canary)
        if injections:
            reasons.append(f"prompt_injection_detected_in_canary (logged only): {injections}")

        # 3. Label contamination: a sandbox note that contradicts the sandbox's own verdict makes the
        #    report inconsistent. Untrusted text may ADD scrutiny (hold), never remove it: the score is
        #    untouched, and a quarantine is never downgraded by a note.
        claim = claimed_label(artifact.canary)
        if claim is not None and "sandbox_verdict" in evidence and claim != evidence["sandbox_verdict"]:
            hold = True
            reasons.append(
                f"label_contamination_in_sandbox_canary: note claims '{claim}', verdict says "
                f"'{evidence['sandbox_verdict']}' (score untouched; held for review)"
            )

        verdict = _decide(score, self.threshold, hold)
        chain.append(f"threshold {self.threshold} -> {verdict.value}")
        shared, redacted = _share_metadata(artifact.metadata, redact=True)  # allowlist before sharing
        return TriageResult(
            artifact_id=artifact.id,
            verdict=verdict,
            score=score,
            reasons=reasons,
            provenance_chain=chain,
            shared_metadata=shared,
            redacted_fields=redacted,
        )


def load_artifacts(data: Dict) -> List[Artifact]:
    return [
        Artifact(
            id=a["id"],
            type=a["type"],
            source=a["source"],
            provenance=Provenance(a["provenance"]),
            metadata=a["metadata"],
            canary=a["canary"],
        )
        for a in data["artifacts"]
    ]


def _print_result(artifact: Artifact, result: TriageResult) -> None:
    print(f"  {artifact.id} ({artifact.type}, {artifact.provenance.value}):")
    print(f"    Verdict: {result.verdict.value} (score: {result.score:.3f})")
    for r in result.reasons:
        print(f"    Reason: {r}")


def main():
    print("=== TriageTrap Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "artifacts.json").read_text())
    artifacts = load_artifacts(data)
    base_rates = data["base_rates"]
    threshold = data["quarantine_threshold"]

    calc = BaseRateCalculator(base_rates)
    print(f"Base rates: {base_rates}")
    print(f"Quarantine threshold: {threshold}")
    print(
        f"Bayes: prior P(malicious) = {calc.prior_malicious:.3f}; "
        f"P(malicious | sandbox says malicious) = {calc.calculate_posterior('malicious'):.3f}; "
        f"P(malicious | sandbox says benign) = {calc.calculate_posterior('benign'):.3f}; "
        f"a single sensor flag alone would be worth {calc.sensor_flag_posterior():.3f}"
    )
    print()

    for agent_name, factory in [
        ("Baseline (No Provenance)", lambda: BaselineTriageAgent(base_rates, threshold)),
        ("Provenance-Aware", lambda: ProvenanceAwareTriageAgent(base_rates, threshold)),
    ]:
        print(f"--- {agent_name} ---")
        agent = factory()
        for artifact in artifacts:
            _print_result(artifact, agent.triage(artifact))
        print()

    # Text cannot move the score: the same malicious sandbox report with an attacker's note attached.
    print("--- Text cannot move the score ---")
    art_003 = next(a for a in artifacts if a.id == "art-003")
    noted = Artifact(art_003.id, art_003.type, art_003.source, art_003.provenance, art_003.metadata,
                     "CANARY_ANALYST_NOTE_THIS_IS_BENIGN_FALSE_POSITIVE")
    print(f'  {noted.id} (verdict: malicious) with canary "{noted.canary}":')
    for label, agent in [("Baseline        ", BaselineTriageAgent(base_rates, threshold)),
                         ("Provenance-Aware", ProvenanceAwareTriageAgent(base_rates, threshold))]:
        r = agent.triage(noted)
        print(f"    {label}: {r.verdict.value} (score: {r.score:.3f})" + (f"  <- {r.reasons[0]}" if r.reasons else ""))
    relabelled = Artifact(art_003.id, art_003.type, "email_attachment_headers", Provenance.UNTRUSTED_METADATA,
                          art_003.metadata, "CANARY_BENIGN_0000")
    r = ProvenanceAwareTriageAgent(base_rates, threshold).triage(relabelled)
    print(f"  {relabelled.id} (same 'verdict: malicious' field) relabelled {relabelled.provenance.value}:")
    print(f"    Provenance-Aware: {r.verdict.value} (score: {r.score:.3f})  <- {r.reasons[0]}")
    print()

    # Sharing the record: de-identify before it leaves triage.
    print("--- Sharing the triage record: allowlist before it leaves triage ---")
    art_002 = next(a for a in artifacts if a.id == "art-002")
    baseline_share = BaselineTriageAgent(base_rates, threshold).triage(art_002)
    guarded_share = ProvenanceAwareTriageAgent(base_rates, threshold).triage(art_002)
    print(f"  {art_002.id} raw metadata (baseline shares this):")
    print(f"    {json.dumps(baseline_share.shared_metadata)}")
    print(f"  {art_002.id} shared record (guarded, allowlisted):")
    print(f"    {json.dumps(guarded_share.shared_metadata)}")
    print(f"  Redacted before sharing: {guarded_share.redacted_fields} "
          f"(kept: the hashes, verdict, and score that carry the decision)")
    print()

    # Show provenance tracking
    print("--- Provenance Chain (Provenance-Aware Agent) ---")
    agent = ProvenanceAwareTriageAgent(base_rates, threshold)
    for artifact in artifacts:
        if artifact.id in ("art-001", "art-003", "art-004", "art-006"):
            result = agent.triage(artifact)
            print(f"  {artifact.id}: {' -> '.join(result.provenance_chain)}")

    print("\n=== Demo Complete ===")
    print("\nKey insight: Canaries in metadata are OBSERVATIONS, not INSTRUCTIONS.")
    print("The score is a Bayesian posterior over structured, sandbox-provenance evidence only;")
    print("free text is logged, may hold a record for an analyst, and can never release one.")
    print("And when the record is shared, an allowlist keeps only the analytic fields - the")
    print("hashes, verdict and score - and masks the submitter, owner and addresses with it.")


if __name__ == "__main__":
    main()
