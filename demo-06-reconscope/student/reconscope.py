#!/usr/bin/env python3
"""
ReconScope - Network Reconnaissance with Provenance Tracking

100% offline: a "probe" reads a JSON fixture that stands in for a network
response. No socket is ever opened (tests/test_reconscope.py proves it).

Two mechanisms, each doing its own work:
  * scope policy  - decides which host:port the agent may look at, BEFORE parsing;
  * provenance    - every field parsed from a response is labelled
                    network_response by the parser itself (structural, never read
                    from the data), and only the provenance-aware agent consults
                    that label before letting a field drive an action.

Injection *marking* is a teaching stand-in: the fixture's `injection` key is the
ground-truth answer, not a detector (Exercise 6.2 replaces it with a heuristic).
"""

import ipaddress
import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Provenance(Enum):
    TRUSTED_CONFIG = "trusted_config"
    USER_INPUT = "user_input"
    NETWORK_RESPONSE = "network_response"


INJECTION_SUFFIX = "_INJECTION_DETECTED"


@dataclass
class ParsedField:
    """A parsed protocol field with provenance."""
    name: str
    value: str
    provenance: Provenance
    source_fixture_id: str

    @property
    def flagged(self) -> bool:
        return self.name.endswith(INJECTION_SUFFIX)


@dataclass
class ScopePolicy:
    """Scope restrictions for recon agent: allow-list of hosts and ports, deny-list of CIDRs/globs."""
    allowed_hosts: List[str]
    allowed_ports: List[int]
    denied_patterns: List[str]

    def host_allowed(self, host: str) -> bool:
        return any(self._match_host_or_cidr(p, host) for p in self.allowed_hosts) and not self.host_denied(host)

    def host_denied(self, host: str) -> bool:
        return any(self._match_host_or_cidr(p, host) for p in self.denied_patterns)

    def allows(self, host: str, port: int) -> bool:
        return self.host_allowed(host) and port in self.allowed_ports

    def explain(self, host: str, port: Optional[int] = None) -> str:
        """Human-readable reason for the decision (for the demo output and audit logs)."""
        reasons = []
        denied = [p for p in self.denied_patterns if self._match_host_or_cidr(p, host)]
        if denied:
            reasons.append(f"host {host} in denied range {denied[0]}")
        elif not any(self._match_host_or_cidr(p, host) for p in self.allowed_hosts):
            reasons.append(f"host {host} not in allowed hosts")
        if port is not None and port not in self.allowed_ports:
            reasons.append(f"port {port} not in allowed ports")
        return "; ".join(reasons) if reasons else "in scope"

    def _match_host_or_cidr(self, pattern: str, host: str) -> bool:
        """Match host against pattern (supports hostname globs and CIDR/IP notation)."""
        # Try CIDR network matching if pattern contains slash or looks like IP
        try:
            network = ipaddress.ip_network(pattern, strict=False)
            if ipaddress.ip_address(host) in network:
                return True
        except ValueError:
            pass

        # Glob / prefix / exact matching
        if pattern.endswith("*"):
            return host.startswith(pattern[:-1])
        if pattern.startswith("*."):
            return host == pattern[2:] or host.endswith(pattern[1:])
        return pattern == host


def parse_source(source: str) -> Tuple[str, int]:
    """'host:port' -> (host, port); a missing port defaults to 80."""
    host, sep, port = source.rpartition(":")
    if not sep:
        return source, 80
    return host, int(port)


_IPV4 = re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})(/\d{1,2})?(?::(\d{1,5}))?\b")
_URL = re.compile(r"https?://([^/:\s'\"]+)(?::(\d{1,5}))?")


def extract_target(text: str) -> Optional[Tuple[str, Optional[int], str]]:
    """Find the first target an instruction refers to (IPv4 address/CIDR or URL host).

    Returns (host, port_or_None, label) where label is the target as written."""
    m = _IPV4.search(text)
    if m:
        return m.group(1), int(m.group(3)) if m.group(3) else None, m.group(0)
    m = _URL.search(text)
    if m:
        return m.group(1), int(m.group(2)) if m.group(2) else None, m.group(1)
    return None


class ProtocolParser:
    """Typed protocol parsers with provenance labelling."""

    def parse(self, fixture: Dict, channel: Provenance = Provenance.NETWORK_RESPONSE) -> List[ParsedField]:
        """Parse a response fixture into typed fields, every one labelled with the channel it came from.

        The label is STRUCTURAL: it is assigned by the parser for the channel being parsed,
        never read from the data (the fixture's own `provenance` key is ignored).
        """
        fields = []
        fixture_id = fixture["id"]

        for field_name, field_value in fixture["fields"].items():
            if isinstance(field_value, dict):
                for sub_name, sub_value in field_value.items():
                    fields.append(ParsedField(f"{field_name}.{sub_name}", str(sub_value), channel, fixture_id))
            elif isinstance(field_value, list):
                for i, item in enumerate(field_value):
                    fields.append(ParsedField(f"{field_name}[{i}]", str(item), channel, fixture_id))
            else:
                fields.append(ParsedField(field_name, str(field_value), channel, fixture_id))

        # Injection MARKING (teaching stand-in for a detector): the fixture's `injection` key is the
        # ground truth; a field containing it is flagged. Real traffic has no such key -> Exercise 6.2.
        ground_truth = fixture.get("injection")
        if ground_truth:
            for f in fields:
                if ground_truth in f.value:
                    f.name += INJECTION_SUFFIX

        return fields


class ReconAgent:
    """Base recon agent: scope check, then parse. Subclasses decide what a flagged field may do."""

    ACTS_ON: Tuple[Provenance, ...] = ()  # which provenance labels may drive an action

    def __init__(self, scope: ScopePolicy):
        self.scope = scope
        self.parser = ProtocolParser()
        self.observations: List[ParsedField] = []
        self.blocked: List[Dict] = []

    def probe(self, fixture: Dict) -> List[ParsedField]:
        """Simulate probing a target: scope check FIRST, then parse the (fixture) response."""
        host, port = parse_source(fixture["source"])

        if not self.scope.allows(host, port):
            reason = self.scope.explain(host, port)
            self.blocked.append({"fixture": fixture["id"], "target": f"{host}:{port}", "reason": reason})
            return [ParsedField("scope_violation", f"{host}:{port} not in scope ({reason})",
                                Provenance.TRUSTED_CONFIG, fixture["id"])]

        fields = self.parser.parse(fixture)
        self.observations.extend(fields)
        return fields

    def decide(self, field: ParsedField) -> Dict:
        """What to do with a field that carries an instruction."""
        if field.provenance in self.ACTS_ON:
            return self.execute(field)
        return {"action": "log", "instruction": field.value, "source": field.name,
                "provenance": field.provenance.value}

    def execute(self, instruction: ParsedField) -> Dict:
        """SIMULATED execution: nothing runs. We record the instruction and, if it names a target,
        what the scope policy would say about the follow-up probe."""
        action = {"action": "execute", "instruction": instruction.value, "source": instruction.name,
                  "provenance": instruction.provenance.value, "simulated": True}
        target = extract_target(instruction.value)
        if target:
            host, port, label = target
            allowed = self.scope.host_allowed(host) and (port is None or port in self.scope.allowed_ports)
            action["follow_up_target"] = label
            action["follow_up_scope"] = "allowed" if allowed else f"blocked ({self.scope.explain(host, port)})"
        return action

    def process(self, fixture: Dict) -> Dict:
        """Probe, then let every flagged field through the agent's decision rule."""
        host, port = parse_source(fixture["source"])
        fields = self.probe(fixture)
        if fields and fields[0].name == "scope_violation":
            return {"fixture": fixture["id"], "scope": "blocked", "reason": self.scope.explain(host, port),
                    "fields": 0, "injections_detected": 0, "actions": []}

        flagged = [f for f in fields if f.flagged]
        return {"fixture": fixture["id"], "scope": "allowed", "fields": len(fields),
                "injections_detected": len(flagged), "actions": [self.decide(f) for f in flagged]}

    def get_observations(self) -> List[Dict]:
        """Get observations as serialisable dicts."""
        return [
            {"name": f.name, "value": f.value, "provenance": f.provenance.value, "source": f.source_fixture_id}
            for f in self.observations
        ]


class VulnerableReconAgent(ReconAgent):
    """Vulnerable: never looks at provenance, so network data becomes instructions."""

    ACTS_ON = (Provenance.TRUSTED_CONFIG, Provenance.USER_INPUT, Provenance.NETWORK_RESPONSE)


class ProvenanceAwareReconAgent(ReconAgent):
    """Provenance-aware: only the operator's configuration or the user may drive actions;
    anything labelled network_response is observation, and is logged, never executed."""

    ACTS_ON = (Provenance.TRUSTED_CONFIG, Provenance.USER_INPUT)


def describe(action: Dict) -> str:
    """One line per decision, for the demo output."""
    if action["action"] == "execute":
        line = f"EXECUTE (simulated) [{action['provenance']}]: {action['instruction'][:60]}"
        if "follow_up_target" in action:
            line += f"\n        -> follow-up probe of {action['follow_up_target']}: {action['follow_up_scope']}"
        return line
    return f"LOG only [{action['provenance']}]: {action['instruction'][:60]}"


def load_fixtures(base_dir: Path) -> Tuple[List[Dict], ScopePolicy]:
    data = json.loads((base_dir / "fixtures" / "protocol_fixtures.json").read_text())
    return data["protocol_fixtures"], ScopePolicy(**data["scope_policy"])


def main():
    print("=== ReconScope Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    fixtures, scope = load_fixtures(base_dir)

    print("Scope Policy:")
    print(f"  Allowed hosts: {scope.allowed_hosts}")
    print(f"  Allowed ports: {scope.allowed_ports}")
    print(f"  Denied patterns: {scope.denied_patterns}")
    print("Injection marking: ground-truth `injection` strings from the fixture (a stand-in for a detector).")
    print("Nothing is executed: EXECUTE lines are simulated decisions, and no socket is ever opened.\n")

    for agent_name, agent_cls in [("Vulnerable Baseline", VulnerableReconAgent),
                                  ("Provenance-Aware", ProvenanceAwareReconAgent)]:
        print(f"--- {agent_name} ---")
        agent = agent_cls(scope)

        for fixture in fixtures:
            result = agent.process(fixture)
            print(f"  {fixture['id']} ({fixture['protocol']}://{fixture['source']}):")
            if result["scope"] == "blocked":
                print(f"    BLOCKED by scope before parsing: {result['reason']}")
                continue
            print(f"    Fields parsed: {result['fields']}, flagged as injection: {result['injections_detected']}")
            for a in result["actions"]:
                print(f"      {describe(a)}")

        print()

    # The switch itself: the same instruction with different provenance
    print("--- Provenance is the switch (Provenance-Aware Agent) ---")
    agent = ProvenanceAwareReconAgent(scope)
    instruction = "scan internal network 10.0.0.0/8"
    for prov in (Provenance.USER_INPUT, Provenance.NETWORK_RESPONSE):
        a = agent.decide(ParsedField("instruction", instruction, prov, "demo"))
        print(f"  \"{instruction}\" as {prov.value:17} -> {describe(a)}")
    print()

    # Show provenance tracking
    print("--- Provenance Tracking (Provenance-Aware Agent) ---")
    agent = ProvenanceAwareReconAgent(scope)
    for fixture in fixtures[:3]:
        agent.probe(fixture)

    for o in agent.get_observations():
        print(f"  {o['source']}.{o['name']} = {o['value'][:50]}... (provenance: {o['provenance']})")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
