#!/usr/bin/env python3
"""
AuthorityBound - Confused Deputy Protection with Provenance & Capability Tokens
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Provenance(Enum):
    TRUSTED_INSTRUCTION = "trusted_instruction"
    USER_DATA = "user_data"
    UNTRUSTED_CONTENT = "untrusted_content"


class Tool(Enum):
    READ_FILE = "read_file"
    SEND_MESSAGE = "send_message"
    UPDATE_RECORD = "update_record"


@dataclass
class CapabilityToken:
    tool: Tool
    scope: str  # e.g., "read:files:/workspace/*"
    issued_to: str  # agent/session identifier


@dataclass
class ToolCall:
    tool: Tool
    args: Dict
    provenance: Provenance
    source_text: str


class PolicyMediator:
    """Mediates tool calls based on capability tokens and provenance."""

    def __init__(self, tokens: List[CapabilityToken], tool_config: Dict):
        self.tokens = {t.tool: t for t in tokens}
        self.tool_config = tool_config

    def authorize(self, call: ToolCall) -> Tuple[bool, str]:
        """Authorize a tool call. Returns (allowed, reason)."""
        # Check provenance: untrusted content cannot invoke high-risk tools
        if call.provenance == Provenance.UNTRUSTED_CONTENT:
            risk = self.tool_config.get(call.tool.value, {}).get("risk", "high")
            if risk in ("medium", "high"):
                return False, f"provenance_{call.provenance.value}_blocks_{risk}_risk_tool"

        # Check capability token
        token = self.tokens.get(call.tool)
        if not token:
            return False, f"no_token_for_{call.tool.value}"

        # Check scope
        if not self._scope_allows(token.scope, call.args):
            return False, f"scope_violation_{token.scope}"

        return True, "authorized"

    def _scope_allows(self, scope: str, args: Dict) -> bool:
        """Check if args are within scope."""
        if scope.endswith("*"):
            prefix = scope[:-1]
            # Check relevant arg fields
            for val in args.values():
                if isinstance(val, str) and val.startswith(prefix):
                    return True
            return False
        # Exact match for specific scopes
        return any(str(v) == scope for v in args.values())


class MockMemory:
    """Memory store with provenance tracking."""

    def __init__(self):
        self.entries = []

    def store(self, content: str, provenance: Provenance, metadata: Dict = None):
        self.entries.append({
            "content": content,
            "provenance": provenance.value,
            "metadata": metadata or {}
        })

    def retrieve(self, query: str) -> List[Dict]:
        # Simple retrieval for demo
        return [e for e in self.entries if query.lower() in e["content"].lower()]


class MockAgent:
    """Agent that processes input through policy mediator."""

    def __init__(self, mediator: PolicyMediator, memory: MockMemory, canaries: Dict):
        self.mediator = mediator
        self.memory = memory
        self.canaries = canaries

    def parse_input(self, text: str, provenance: Provenance) -> List[ToolCall]:
        """Parse input text into tool calls with provenance."""
        calls = []

        # Simple pattern matching for demo
        text_lower = text.lower()
        if "read_file" in text_lower or "read file" in text_lower or text_lower.startswith("read "):
            # Find file-like patterns in text
            patterns = re.findall(r'[\w./\-]+\.\w+|/\w+(?:/\w+)*', text)
            path = patterns[0] if patterns else "README.md"
            # Prepend workspace for relative paths
            if not path.startswith('/'):
                path = '/workspace/' + path
            calls.append(ToolCall(Tool.READ_FILE, {"path": path}, provenance, text))

        if "send_message" in text_lower or "send message" in text_lower:
            calls.append(ToolCall(Tool.SEND_MESSAGE, {"to": "admin", "body": "test"}, provenance, text))

        if "update_record" in text_lower or "update record" in text_lower:
            calls.append(ToolCall(Tool.UPDATE_RECORD, {"table": "users", "data": {}}, provenance, text))

        return calls

    def process(self, text: str, provenance: Provenance) -> Dict:
        """Process input and execute authorized tool calls."""
        self.memory.store(text, provenance)
        calls = self.parse_input(text, provenance)

        results = []
        for call in calls:
            allowed, reason = self.mediator.authorize(call)
            if allowed:
                results.append({"tool": call.tool.value, "status": "executed", "args": call.args})
            else:
                results.append({"tool": call.tool.value, "status": "blocked", "reason": reason})

        return {"input": text, "provenance": provenance.value, "results": results}


def create_baseline_agent() -> MockAgent:
    """Baseline: No provenance checks, no capability tokens."""
    # All tools allowed, no provenance filtering
    tokens = [
        CapabilityToken(Tool.READ_FILE, "*", "baseline"),
        CapabilityToken(Tool.SEND_MESSAGE, "*", "baseline"),
        CapabilityToken(Tool.UPDATE_RECORD, "*", "baseline"),
    ]
    tool_config = {
        "read_file": {"risk": "low"},
        "send_message": {"risk": "medium"},
        "update_record": {"risk": "high"}
    }
    mediator = PolicyMediator(tokens, tool_config)
    # Override authorize to ignore provenance
    original_authorize = mediator.authorize
    def permissive_authorize(call):
        token = mediator.tokens.get(call.tool)
        if token and mediator._scope_allows(token.scope, call.args):
            return True, "authorized"
        return False, "no_token"
    mediator.authorize = permissive_authorize

    return MockAgent(mediator, MockMemory(), {})


def create_provenance_aware_agent() -> MockAgent:
    """Provenance-aware: Blocks untrusted content from high-risk tools."""
    tokens = [
        CapabilityToken(Tool.READ_FILE, "/workspace/*", "prov_agent"),
        CapabilityToken(Tool.SEND_MESSAGE, "internal/*", "prov_agent"),
        CapabilityToken(Tool.UPDATE_RECORD, "app/*", "prov_agent"),
    ]
    tool_config = {
        "read_file": {"risk": "low"},
        "send_message": {"risk": "medium"},
        "update_record": {"risk": "high"}
    }
    mediator = PolicyMediator(tokens, tool_config)
    return MockAgent(mediator, MockMemory(), {})


def create_scope_bound_agent() -> MockAgent:
    """Scope-bound: Strict scope enforcement + provenance."""
    return create_provenance_aware_agent()  # Same for demo


def main():
    data = json.loads(Path("fixtures/authoritybound.json").read_text())
    canaries = data["canaries"]
    scenarios = data["scenarios"]

    print("=== AuthorityBound Demo ===\n")

    for agent_name, factory in [
        ("Unguarded Baseline", create_baseline_agent),
        ("Provenance-Aware", create_provenance_aware_agent),
        ("Scope-Bound Mediator", create_scope_bound_agent)
    ]:
        print(f"--- {agent_name} ---")
        agent = factory()

        for scenario in scenarios:
            provenance = Provenance(scenario["provenance"])
            result = agent.process(scenario["input"], provenance)

            print(f"  {scenario['id']}:")
            for r in result["results"]:
                status = "✓" if r["status"] == "executed" else "✗"
                print(f"    {status} {r['tool']}: {r['status']} ({r.get('reason', 'ok')})")

        print()


if __name__ == "__main__":
    main()