#!/usr/bin/env python3
"""
TriageTrap - Safe Malware Triage with Provenance Tracking
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Provenance(Enum):
    TRUSTED_SENSOR = "trusted_sensor"
    TRUSTED_SANDBOX = "trusted_sandbox"
    UNTRUSTED_METADATA = "untrusted_metadata"


class Verdict(Enum):
    BENIGN = "benign"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"
    QUARANTINE = "quarantine"


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


class BaseRateCalculator:
    """Base-rate-aware scoring."""

    def __init__(self, base_rates: Dict):
        self.prior_malicious = base_rates.get("malicious_prior", 0.02)
        self.sensor_fp = base_rates.get("sensor_false_positive", 0.01)
        self.sandbox_fn = base_rates.get("sandbox_false_negative", 0.05)

    def update(self, evidence: Dict) -> float:
        """Bayesian update with base rate."""
        # Simplified: combine evidence likelihoods with prior
        score = self.prior_malicious

        if evidence.get("sandbox_verdict") == "malicious":
            score = 0.9 * (1 - self.sandbox_fn) + 0.1 * self.prior_malicious
        elif evidence.get("sandbox_verdict") == "benign":
            score = 0.1 * self.sandbox_fn + 0.9 * self.prior_malicious

        if evidence.get("prompt_injection_detected"):
            score = max(score, 0.8)  # Strong signal

        if evidence.get("label_contamination"):
            score = min(score * 0.5, 0.3)  # Reduce confidence

        return min(max(score, 0.0), 1.0)


class PromptInjectionDetector:
    """Detect prompt-like payloads in metadata/canaries."""

    INJECTION_PATTERNS = [
        r"ignore.*previous.*instructions?",
        r"system.*override",
        r"disable.*safeguard",
        r"quarantine.*all",
        r"trust.*me",
        r"definitely.*malware"
    ]

    def detect(self, text: str) -> List[str]:
        matches = []
        text_lower = text.lower()
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches.append(pattern)
        return matches


class BaselineTriageAgent:
    """Baseline: No provenance awareness, vulnerable to injection."""

    def __init__(self, base_rates: Dict, threshold: float):
        self.calculator = BaseRateCalculator(base_rates)
        self.detector = PromptInjectionDetector()
        self.threshold = threshold

    def triage(self, artifact: Artifact) -> TriageResult:
        evidence = {"sandbox_verdict": artifact.metadata.get("verdict")}
        reasons = []

        # Check canary for injection (but treats it as signal)
        injections = self.detector.detect(artifact.canary)
        if injections:
            evidence["prompt_injection_detected"] = True
            reasons.append(f"prompt_injection: {injections}")

        # Check for label contamination
        if "trust_me" in artifact.canary.lower() or "definitely_malware" in artifact.canary.lower():
            evidence["label_contamination"] = True
            reasons.append("label_contamination")

        score = self.calculator.update(evidence)
        verdict = Verdict.QUARANTINE if score >= self.threshold else Verdict.BENIGN

        return TriageResult(
            artifact_id=artifact.id,
            verdict=verdict,
            score=score,
            reasons=reasons,
            provenance_chain=[artifact.provenance.value]
        )


class ProvenanceAwareTriageAgent:
    """Provenance-aware: Separates observation from instruction."""

    def __init__(self, base_rates: Dict, threshold: float):
        self.calculator = BaseRateCalculator(base_rates)
        self.detector = PromptInjectionDetector()
        self.threshold = threshold

    def triage(self, artifact: Artifact) -> TriageResult:
        evidence = {"sandbox_verdict": artifact.metadata.get("verdict")}
        reasons = []

        # Check canary for injection - LOG ONLY, don't use as evidence
        injections = self.detector.detect(artifact.canary)
        if injections:
            reasons.append(f"prompt_injection_detected_in_canary (logged only): {injections}")
            # DO NOT add to evidence - canary is untrusted metadata

        # Check for label contamination in sandbox verdict
        if artifact.provenance == Provenance.TRUSTED_SANDBOX:
            if "trust_me" in artifact.canary.lower() or "definitely_malware" in artifact.canary.lower():
                reasons.append("label_contamination_in_sandbox_canary (reducing confidence)")
                evidence["label_contamination"] = True

        score = self.calculator.update(evidence)
        verdict = Verdict.QUARANTINE if score >= self.threshold else Verdict.BENIGN

        return TriageResult(
            artifact_id=artifact.id,
            verdict=verdict,
            score=score,
            reasons=reasons,
            provenance_chain=[artifact.provenance.value, "calculator", "threshold"]
        )


def main():
    print("=== TriageTrap Demo ===\n")

    data = json.loads(Path("fixtures/artifacts.json").read_text())
    artifacts_data = data["artifacts"]
    base_rates = data["base_rates"]
    threshold = data["quarantine_threshold"]

    artifacts = []
    for a in artifacts_data:
        artifacts.append(Artifact(
            id=a["id"],
            type=a["type"],
            source=a["source"],
            provenance=Provenance(a["provenance"]),
            metadata=a["metadata"],
            canary=a["canary"]
        ))

    print(f"Base rates: {base_rates}")
    print(f"Quarantine threshold: {threshold}")
    print()

    for agent_name, factory in [
        ("Baseline (No Provenance)", lambda: BaselineTriageAgent(base_rates, threshold)),
        ("Provenance-Aware", lambda: ProvenanceAwareTriageAgent(base_rates, threshold))
    ]:
        print(f"--- {agent_name} ---")
        agent = factory()

        for artifact in artifacts:
            result = agent.triage(artifact)
            print(f"  {artifact.id} ({artifact.type}, {artifact.provenance.value}):")
            print(f"    Verdict: {result.verdict.value} (score: {result.score:.2f})")
            for r in result.reasons:
                print(f"    Reason: {r}")

        print()

    # Show provenance tracking
    print("--- Provenance Chain (Provenance-Aware Agent) ---")
    agent = ProvenanceAwareTriageAgent(base_rates, threshold)
    for artifact in artifacts[:3]:
        result = agent.triage(artifact)
        print(f"  {artifact.id}: {' -> '.join(result.provenance_chain)}")

    print("\n=== Demo Complete ===")
    print("\nKey insight: Canaries in metadata are OBSERVATIONS, not INSTRUCTIONS.")
    print("Provenance-aware agent logs injections but doesn't act on them.")


if __name__ == "__main__":
    main()