#!/usr/bin/env python3
"""
InterceptBound - Traffic Interception & Taint Tracking
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


class Provenance(Enum):
    TRUSTED_LOCAL = "trusted_local"
    USER_SUPPLIED = "user_supplied"
    INTERCEPTED_NETWORK = "intercepted_network"


class TaintLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ParsedField:
    name: str
    value: Any
    provenance: Provenance
    taint: TaintLevel
    source_frame: str


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
    injection: Optional[str]


class TaintTracker:
    """Tracks taint through parsing and processing."""

    def __init__(self, default_taint: TaintLevel = TaintLevel.HIGH):
        self.default_taint = default_taint

    def parse_frame(self, frame: TrafficFrame) -> List[ParsedField]:
        """Parse frame and assign taint to every field."""
        parsed = []
        for field_name, field_value in frame.fields.items():
            if isinstance(field_value, dict):
                for sub_name, sub_value in field_value.items():
                    parsed.append(ParsedField(
                        name=f"{field_name}.{sub_name}",
                        value=sub_value,
                        provenance=frame.provenance,
                        taint=frame.taint,
                        source_frame=frame.id
                    ))
            elif isinstance(field_value, list):
                for i, item in enumerate(field_value):
                    if isinstance(item, dict):
                        for sub_name, sub_value in item.items():
                            parsed.append(ParsedField(
                                name=f"{field_name}[{i}].{sub_name}",
                                value=sub_value,
                                provenance=frame.provenance,
                                taint=frame.taint,
                                source_frame=frame.id
                            ))
                    else:
                        parsed.append(ParsedField(
                            name=f"{field_name}[{i}]",
                            value=item,
                            provenance=frame.provenance,
                            taint=frame.taint,
                            source_frame=frame.id
                        ))
            else:
                parsed.append(ParsedField(
                    name=field_name,
                    value=field_value,
                    provenance=frame.provenance,
                    taint=frame.taint,
                    source_frame=frame.id
                ))

        # Mark injection fields
        if frame.injection:
            for p in parsed:
                if frame.injection in str(p.value):
                    p.name += "_INJECTION"
            # Also add injection as a separate field for detection
            parsed.append(ParsedField(
                name="injection",
                value=frame.injection,
                provenance=frame.provenance,
                taint=frame.taint,
                source_frame=frame.id
            ))

        return parsed


class EphemeralBuffer:
    """Ephemeral buffer with secure deletion."""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 60, secure_delete: bool = True):
        self.buffer = deque(maxlen=max_size)
        self.ttl = ttl_seconds
        self.secure_delete = secure_delete
        self.timestamps = {}

    def add(self, key: str, data: Any):
        """Add data to buffer."""
        self.buffer.append(key)
        self.timestamps[key] = {"data": data, "added": time.time()}

    def get(self, key: str) -> Optional[Any]:
        """Get data if not expired."""
        if key not in self.timestamps:
            return None
        entry = self.timestamps[key]
        if time.time() - entry["added"] > self.ttl:
            self.delete(key)
            return None
        return entry["data"]

    def delete(self, key: str):
        """Secure delete."""
        if key in self.timestamps:
            if self.secure_delete:
                # Overwrite in memory (simulated)
                self.timestamps[key]["data"] = "[SECURELY DELETED]"
            del self.timestamps[key]
            # Remove from buffer
            try:
                self.buffer.remove(key)
            except ValueError:
                pass

    def cleanup_expired(self):
        """Remove expired entries."""
        now = time.time()
        expired = [k for k, v in self.timestamps.items() if now - v["added"] > self.ttl]
        for k in expired:
            self.delete(k)


class ActionGuard:
    """Downstream action guard - blocks tainted values from sensitive ops."""

    def __init__(self, max_taint_for_action: TaintLevel | str = TaintLevel.LOW):
        if isinstance(max_taint_for_action, str):
            self.max_taint = TaintLevel(max_taint_for_action)
        else:
            self.max_taint = max_taint_for_action

    def authorize(self, action: str, required_taint: TaintLevel, data: Any, provenance: Provenance) -> tuple[bool, str]:
        """Authorize action based on taint level."""
        taint_order = {TaintLevel.LOW: 0, TaintLevel.MEDIUM: 1, TaintLevel.HIGH: 2}

        if taint_order[required_taint] > taint_order[self.max_taint]:
            return False, f"taint_too_high: {required_taint.value} > {self.max_taint.value}"

        if provenance == Provenance.INTERCEPTED_NETWORK and required_taint != TaintLevel.LOW:
            return False, f"intercepted_network_requires_low_taint"

        return True, "authorized"


class BaselineAgent:
    """Baseline: No taint tracking, executes everything."""

    def __init__(self):
        self.buffer = EphemeralBuffer()

    def process(self, frame: TrafficFrame) -> Dict:
        # Parse without taint
        actions = []
        frame_str = str(frame.fields) + " " + (frame.injection or "")
        if frame.protocol == "http" and "token" in str(frame.fields):
            actions.append({"action": "store_token", "data": frame.fields})
        if frame.protocol == "dns" and "TXT" in str(frame.fields):
            actions.append({"action": "update_dns_cache", "data": frame.fields})
        if "shutdown" in frame_str:
            actions.append({"action": "execute_shutdown", "data": frame.fields})

        return {"frame": frame.id, "actions": actions, "taint_tracked": False}


class TaintAwareAgent:
    """Taint-aware: Tracks provenance and taint, guards actions."""

    def __init__(self, scope_policy: Dict, buffer_config: Dict):
        self.tracker = TaintTracker()
        self.buffer = EphemeralBuffer(**buffer_config)
        max_taint_str = scope_policy.get("max_taint_for_action", "low")
        max_taint = TaintLevel(max_taint_str) if isinstance(max_taint_str, str) else max_taint_str
        self.guard = ActionGuard(max_taint)
        self.allowed_sources = scope_policy.get("allowed_sources", [])
        self.allowed_destinations = scope_policy.get("allowed_destinations", [])

    def process(self, frame: TrafficFrame) -> Dict:
        # Check scope - extract IP from source (without port)
        src_ip = frame.src.split(":")[0] if ":" in frame.src else frame.src
        if src_ip not in self.allowed_sources:
            return {"frame": frame.id, "actions": [], "blocked": "source_not_allowed"}

        # Parse with taint tracking
        parsed = self.tracker.parse_frame(frame)

        # Store in ephemeral buffer
        for p in parsed:
            self.buffer.add(f"{frame.id}.{p.name}", p)

        # Determine actions with guard
        actions = []
        blocked = []

        for p in parsed:
            field_taint = p.taint
            
            if "token" in str(p.value) and p.provenance == Provenance.INTERCEPTED_NETWORK:
                allowed, reason = self.guard.authorize("store_credential", field_taint, p.value, p.provenance)
                if allowed:
                    actions.append({"action": "store_token", "field": p.name})
                else:
                    blocked.append({"action": "store_token", "reason": reason})

            if "shutdown" in p.name or "shutdown" in str(p.value):
                allowed, reason = self.guard.authorize("system_shutdown", field_taint, p.value, p.provenance)
                if allowed:
                    actions.append({"action": "execute_shutdown"})
                else:
                    blocked.append({"action": "execute_shutdown", "reason": reason})

            if p.name.endswith("_INJECTION"):
                blocked.append({"action": "process_injection", "field": p.name, "reason": "injection_detected"})

        return {
            "frame": frame.id,
            "actions": actions,
            "blocked": blocked,
            "parsed_fields": len(parsed),
            "taint_tracked": True
        }


def main():
    print("=== InterceptBound Demo ===\n")

    data = json.loads(Path("fixtures/traffic.json").read_text())
    frames_data = data["traffic_frames"]
    scope = data["scope_policy"]
    buffer_config = data["ephemeral_buffer"]

    frames = []
    for f in frames_data:
        frames.append(TrafficFrame(
            id=f["id"],
            protocol=f["protocol"],
            src=f["src"],
            dst=f["dst"],
            direction=f["direction"],
            fields=f["fields"],
            provenance=Provenance(f["provenance"]),
            taint=TaintLevel(f["taint"]),
            injection=f["injection"]
        ))

    print("Scope Policy:")
    print(f"  Allowed sources: {scope['allowed_sources']}")
    print(f"  Max taint for action: {scope['max_taint_for_action']}")
    print()

    for agent_name, factory in [
        ("Unguarded Baseline", lambda: BaselineAgent()),
        ("Taint-Aware Guarded", lambda: TaintAwareAgent(scope, buffer_config))
    ]:
        print(f"--- {agent_name} ---")
        agent = factory()

        for frame in frames:
            result = agent.process(frame)
            print(f"  {frame.id} ({frame.protocol} {frame.src}->{frame.dst}):")
            if result.get("blocked"):
                for b in result["blocked"]:
                    print(f"    BLOCKED: {b['action']} ({b.get('reason', 'scope')})")
            for a in result.get("actions", []):
                print(f"    ALLOWED: {a['action']}")

        print()

    # Show taint tracking
    print("--- Taint Tracking (Taint-Aware Agent) ---")
    agent = TaintAwareAgent(scope, buffer_config)
    frame = frames[0]  # HTTP with token
    result = agent.process(frame)
    print(f"Frame {frame.id}: parsed {result['parsed_fields']} fields with taint")

    # Show buffer behavior
    print("\n--- Ephemeral Buffer ---")
    buffer = EphemeralBuffer(secure_delete=True)
    buffer.add("test_key", "sensitive_token_data")
    print(f"Stored: {buffer.get('test_key')}")
    buffer.delete("test_key")
    print(f"After delete: {buffer.get('test_key')}")

    print("\n=== Demo Complete ===")
    print("\nKey insight: Intercepted network data is OBSERVATION, not INSTRUCTION.")
    print("Taint tracking prevents forged/tainted data from driving sensitive actions.")


if __name__ == "__main__":
    main()