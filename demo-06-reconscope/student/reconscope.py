#!/usr/bin/env python3
"""
ReconScope - Network Reconnaissance with Provenance Tracking
"""

import json
import re
import ipaddress
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class Provenance(Enum):
    TRUSTED_CONFIG = "trusted_config"
    USER_INPUT = "user_input"
    NETWORK_RESPONSE = "network_response"


@dataclass
class ParsedField:
    """A parsed protocol field with provenance."""
    name: str
    value: str
    provenance: Provenance
    source_fixture_id: str


@dataclass
class ScopePolicy:
    """Scope restrictions for recon agent."""
    allowed_hosts: List[str]
    allowed_ports: List[int]
    denied_patterns: List[str]

    def allows(self, host: str, port: int) -> bool:
        # Check allowed
        host_allowed = any(self._match_host(pattern, host) for pattern in self.allowed_hosts)
        port_allowed = port in self.allowed_ports

        # Check denied
        host_denied = any(self._match_cidr(pattern, host) for pattern in self.denied_patterns)

        return host_allowed and port_allowed and not host_denied

    def _match_host(self, pattern: str, host: str) -> bool:
        if pattern.endswith("*"):
            return host.startswith(pattern[:-1])
        return pattern == host

    def _match_cidr(self, pattern: str, host: str) -> bool:
        try:
            network = ipaddress.ip_network(pattern, strict=False)
            return ipaddress.ip_address(host) in network
        except Exception:
            return False


class ProtocolParser:
    """Typed protocol parsers with provenance labeling."""

    def parse(self, fixture: Dict) -> List[ParsedField]:
        """Parse fixture and label every field with provenance."""
        fields = []
        provenance = Provenance(fixture["provenance"])
        fixture_id = fixture["id"]

        for field_name, field_value in fixture["fields"].items():
            if isinstance(field_value, dict):
                for sub_name, sub_value in field_value.items():
                    fields.append(ParsedField(
                        name=f"{field_name}.{sub_name}",
                        value=str(sub_value),
                        provenance=provenance,
                        source_fixture_id=fixture_id
                    ))
            elif isinstance(field_value, list):
                for i, item in enumerate(field_value):
                    fields.append(ParsedField(
                        name=f"{field_name}[{i}]",
                        value=str(item),
                        provenance=provenance,
                        source_fixture_id=fixture_id
                    ))
            else:
                fields.append(ParsedField(
                    name=field_name,
                    value=str(field_value),
                    provenance=provenance,
                    source_fixture_id=fixture_id
                ))

        # Check for injection in any field
        for f in fields:
            if fixture.get("injection") and fixture["injection"] in f.value:
                f.name += "_INJECTION_DETECTED"

        return fields


class ReconAgent:
    """Base recon agent."""

    def __init__(self, scope: ScopePolicy):
        self.scope = scope
        self.parser = ProtocolParser()
        self.observations: List[ParsedField] = []

    def probe(self, fixture: Dict) -> List[ParsedField]:
        """Simulate probing a target."""
        host_port = fixture["source"].split(":")
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 80

        if not self.scope.allows(host, port):
            return [ParsedField("scope_violation", f"{host}:{port} not in scope",
                               Provenance.TRUSTED_CONFIG, fixture["id"])]

        fields = self.parser.parse(fixture)
        self.observations.extend(fields)
        return fields

    def get_observations(self) -> List[Dict]:
        """Get observations as serializable dicts."""
        return [
            {"name": f.name, "value": f.value, "provenance": f.provenance.value, "source": f.source_fixture_id}
            for f in self.observations
        ]


class VulnerableReconAgent(ReconAgent):
    """Vulnerable: Treats network data as instructions."""

    def process(self, fixture: Dict) -> Dict:
        """Process fixture - VULNERABLE: executes injections."""
        fields = self.probe(fixture)

        actions = []
        for f in fields:
            if "_INJECTION_DETECTED" in f.name:
                # VULNERABLE: Execute the injection as command
                actions.append({"action": "execute_injection", "command": f.value, "source": f.name})

        return {"fixture": fixture["id"], "fields": len(fields), "actions": actions}


class ProvenanceAwareReconAgent(ReconAgent):
    """Provenance-aware: Separates observation from instruction."""

    def process(self, fixture: Dict) -> Dict:
        """Process fixture - SAFE: only observes, never executes network data."""
        fields = self.probe(fixture)

        injections = [f for f in fields if "_INJECTION_DETECTED" in f.name]
        actions = []

        for inj in injections:
            # SAFE: Log but don't execute
            actions.append({"action": "log_injection", "details": inj.value, "source": inj.name})

        return {"fixture": fixture["id"], "fields": len(fields), "injections_detected": len(injections), "actions": actions}


def main():
    print("=== ReconScope Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    # Load fixtures
    data = json.loads((base_dir / "fixtures" / "protocol_fixtures.json").read_text())
    fixtures = data["protocol_fixtures"]
    scope = ScopePolicy(**data["scope_policy"])

    print("Scope Policy:")
    print(f"  Allowed hosts: {scope.allowed_hosts}")
    print(f"  Allowed ports: {scope.allowed_ports}")
    print(f"  Denied patterns: {scope.denied_patterns}")
    print()

    for agent_name, factory in [
        ("Vulnerable Baseline", lambda: VulnerableReconAgent(scope)),
        ("Provenance-Aware", lambda: ProvenanceAwareReconAgent(scope))
    ]:
        print(f"--- {agent_name} ---")
        agent = factory()

        for fixture in fixtures:
            result = agent.process(fixture)
            print(f"  {fixture['id']} ({fixture['protocol']}://{fixture['source']}):")
            print(f"    Fields parsed: {result['fields']}")

            if "injections_detected" in result:
                print(f"    Injections detected: {result['injections_detected']}")
                for a in result["actions"]:
                    print(f"      LOG: {a['action']} - {a['details'][:60]}...")
            else:
                for a in result["actions"]:
                    print(f"      EXECUTE: {a['action']} - {a['command'][:60]}...")

        print()

    # Show provenance tracking
    print("--- Provenance Tracking (Provenance-Aware Agent) ---")
    agent = ProvenanceAwareReconAgent(scope)
    for fixture in fixtures[:3]:
        agent.probe(fixture)

    obs = agent.get_observations()
    for o in obs:
        print(f"  {o['source']}.{o['name']} = {o['value'][:50]}... (provenance: {o['provenance']})")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()