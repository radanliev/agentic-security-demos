#!/usr/bin/env python3
"""
InclusionTrap - File Inclusion & Scope Boundaries
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Provenance(Enum):
    FILE_SYSTEM = "file_system"
    SIMULATED_REMOTE = "simulated_remote"
    TRUSTED_CONFIG = "trusted_config"
    USER_INPUT = "user_input"


@dataclass
class InclusionResult:
    scenario_id: str
    included_content: str
    provenance: Provenance
    action: str  # "allowed", "blocked", "executed"
    reason: str


class InjectionDetector:
    """Detect prompt injections in included content."""

    PATTERNS = [
        r"ignore.*previous.*instructions?",
        r"system.*override",
        r"send.*all.*logs",
        r"rm\s+-rf",
        r"exec\s*\(",
        r"eval\s*\(",
        r"subprocess"
    ]

    def detect(self, content: str) -> List[str]:
        matches = []
        for pattern in self.PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                matches.append(pattern)
        return matches


class ScopePolicy:
    """File system scope policy."""

    def __init__(self, allowed: List[str], denied: List[str]):
        self.allowed = allowed
        self.denied = denied

    def can_read(self, path: str) -> bool:
        # Check denied first
        for pattern in self.denied:
            if self._match(pattern, path):
                return False
        # Check allowed
        for pattern in self.allowed:
            if self._match(pattern, path):
                return True
        return False

    def _match(self, pattern: str, path: str) -> bool:
        if pattern.endswith("*"):
            return path.startswith(pattern[:-1])
        return pattern == path


class VulnerableInclusionAgent:
    """Vulnerable: Includes and executes file content."""

    def __init__(self, files: Dict, scope: ScopePolicy):
        self.files = files
        self.scope = scope
        self.detector = InjectionDetector()

    def process(self, scenario: Dict) -> InclusionResult:
        # Extract path from request
        path_match = re.search(r'[?&]file=([^&]+)|[?&]url=([^&]+)', scenario["request"])
        if path_match:
            path = path_match.group(1) or path_match.group(2)
        else:
            path = ""

        # Resolve path (simulated)
        if path.startswith("http"):
            # Simulated remote
            content = scenario["included_content"]
            provenance = Provenance.SIMULATED_REMOTE
        else:
            # Local file
            resolved = self._resolve_path(path)
            content = self.files.get(resolved, "")
            provenance = Provenance.FILE_SYSTEM

        # VULNERABLE: Check for injection but still execute
        injections = self.detector.detect(content)
        if injections:
            # Still executes!
            return InclusionResult(
                scenario_id=scenario["id"],
                included_content=content[:100],
                provenance=provenance,
                action="executed",
                reason=f"injection_detected_but_executed: {injections}"
            )

        return InclusionResult(
            scenario_id=scenario["id"],
            included_content=content[:100],
            provenance=provenance,
            action="allowed",
            reason="no_injection"
        )

    def _resolve_path(self, path: str) -> str:
        """Resolve path with traversal (vulnerable)."""
        # Simple resolution for demo - normalize path
        if path.startswith("../"):
            # Path traversal - vulnerable!
            parts = path.split("/")
            resolved_parts = []
            for part in parts:
                if part == "..":
                    if resolved_parts:
                        resolved_parts.pop()
                elif part and part != ".":
                    resolved_parts.append(part)
            return "/" + "/".join(resolved_parts)
        # Handle relative paths without traversal
        if not path.startswith("/"):
            return "/app/" + path
        return path


class GuardedInclusionAgent:
    """Guarded: Provenance checks, scope enforcement, no execution of included content."""

    def __init__(self, files: Dict, scope: ScopePolicy):
        self.files = files
        self.scope = scope
        self.detector = InjectionDetector()

    def process(self, scenario: Dict) -> InclusionResult:
        path_match = re.search(r'[?&]file=([^&]+)|[?&]url=([^&]+)', scenario["request"])
        if path_match:
            path = path_match.group(1) or path_match.group(2)
        else:
            path = ""

        # Determine provenance and content
        if path.startswith("http"):
            content = scenario["included_content"]
            provenance = Provenance.SIMULATED_REMOTE
            source_path = path
        else:
            resolved = self._resolve_path(path)
            content = self.files.get(resolved, "")
            provenance = Provenance.FILE_SYSTEM
            source_path = resolved

        # Check injection in both file content and scenario's included_content
        check_content = content or scenario.get("included_content", "")
        
        # 1. Injection detection (check regardless of scope)
        injections = self.detector.detect(check_content)
        if injections:
            return InclusionResult(
                scenario_id=scenario["id"],
                included_content=content[:100] if content else scenario.get("included_content", "")[:100],
                provenance=provenance,
                action="blocked",
                reason=f"injection_detected: {injections}"
            )

        # 2. Scope check
        if not self.scope.can_read(source_path):
            return InclusionResult(
                scenario_id=scenario["id"],
                included_content=content[:100],
                provenance=provenance,
                action="blocked",
                reason=f"scope_violation: {source_path} not in allowed paths"
            )

        # 3. Content type check - never execute included content
        # Only render/read, never exec
        return InclusionResult(
            scenario_id=scenario["id"],
            included_content=content[:100],
            provenance=provenance,
            action="allowed",
            reason="safe_content_read_only"
        )

    def _resolve_path(self, path: str) -> str:
        """Safe canonical path resolution with traversal detection."""
        import posixpath
        import urllib.parse

        # Decode URL-encoded traversals
        decoded = urllib.parse.unquote(path)

        # Detect traversal patterns
        if decoded.startswith("../") or "/../" in decoded or decoded.endswith("/..") or decoded == "..":
            return "/blocked/traversal"

        # Canonical normalization
        if not decoded.startswith("/"):
            canonical = posixpath.normpath(posixpath.join("/app", decoded))
        else:
            canonical = posixpath.normpath(decoded)

        # Ensure canonical path stays within root if relative was provided
        if not decoded.startswith("/") and not canonical.startswith("/app"):
            return "/blocked/traversal"

        return canonical


def main():
    print("=== InclusionTrap Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "inclusion.json").read_text())
    files = data["files"]
    scenarios = data["inclusion_scenarios"]
    scope = ScopePolicy(
        data["agent_scope"]["allowed_read_paths"],
        data["agent_scope"]["denied_read_paths"]
    )

    print("Agent Scope:")
    print(f"  Allowed: {scope.allowed}")
    print(f"  Denied: {scope.denied}")
    print()

    for agent_name, factory in [
        ("Vulnerable Baseline", lambda: VulnerableInclusionAgent(files, scope)),
        ("Guarded (Scope + Provenance)", lambda: GuardedInclusionAgent(files, scope))
    ]:
        print(f"--- {agent_name} ---")
        agent = factory()

        for scenario in scenarios:
            result = agent.process(scenario)
            status = "✓" if result.action in ("allowed", "blocked") else "✗ VULNERABLE"
            print(f"  {scenario['id']}: {status}")
            print(f"    Action: {result.action} ({result.reason})")
            if result.action == "executed":
                print(f"    ⚠️  EXECUTED INCLUDED CONTENT!")

        print()

    print("=== Demo Complete ===")
    print("\nKey lesson: READING content ≠ GRANTING authority.")
    print("Included files are DATA. Only explicit, verified INSTRUCTIONS drive actions.")


if __name__ == "__main__":
    main()