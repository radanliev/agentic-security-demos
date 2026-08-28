#!/usr/bin/env python3
"""
AuthorityBound - Confused Deputy Protection with Provenance & Capability Tokens

Two independent defenses, combined in one mediator:

* Provenance  -- WHO authored the instruction?  Untrusted content may never
                 drive a medium- or high-risk tool, whatever it says.
* Scope       -- WHAT may this tool touch?  A capability token grants a tool
                 over a scope ("/workspace/*"), checked against the tool's
                 designated argument (path / recipient / table).

Three agents share the same parser and the same mediator code; they differ
only in mediator configuration, so the attack matrix is a controlled
comparison:

    baseline    provenance ignored,  wildcard tokens
    provenance  provenance enforced, wildcard tokens
    scope       provenance enforced, narrow tokens
"""

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "authoritybound.json"


class Provenance(Enum):
    TRUSTED_INSTRUCTION = "trusted_instruction"
    USER_DATA = "user_data"
    UNTRUSTED_CONTENT = "untrusted_content"


class Tool(Enum):
    READ_FILE = "read_file"
    SEND_MESSAGE = "send_message"
    UPDATE_RECORD = "update_record"


# Risk tier and the argument a scope is checked against. Loaded from the fixture's
# tool registry by the factories; the defaults keep hand-built mediators working.
DEFAULT_TOOL_CONFIG: Dict[str, Dict[str, str]] = {
    "read_file": {"risk": "low", "scope_arg": "path"},
    "send_message": {"risk": "medium", "scope_arg": "to"},
    "update_record": {"risk": "high", "scope_arg": "table"},
}


def load_tool_config(path: Path = FIXTURE_PATH) -> Dict[str, Dict[str, str]]:
    return json.loads(path.read_text())["tools"]


@dataclass
class CapabilityToken:
    tool: Tool
    scope: str  # "*" (anything), "prefix*" (textual prefix), or an exact value
    issued_to: str  # agent/session identifier


@dataclass
class ToolCall:
    tool: Tool
    args: Dict
    provenance: Provenance
    source_text: str


class PolicyMediator:
    """Mediates tool calls based on capability tokens and provenance.

    The token table is the mediator's own grant list: nothing in the agent's
    input can add to it. Every decision path that lacks information denies.
    """

    def __init__(self, tokens: List[CapabilityToken], tool_config: Dict,
                 check_provenance: bool = True):
        self.tokens = {t.tool: t for t in tokens}
        self.tool_config = tool_config
        self.check_provenance = check_provenance

    def authorize(self, call: ToolCall) -> Tuple[bool, str]:
        """Authorize a tool call. Returns (allowed, reason)."""
        cfg = self.tool_config.get(call.tool.value, {})
        risk = cfg.get("risk", "high")  # unknown tool: treat as high risk

        # 1. Provenance: untrusted content cannot invoke medium/high-risk tools.
        if self.check_provenance and call.provenance == Provenance.UNTRUSTED_CONTENT:
            if risk in ("medium", "high"):
                return False, f"provenance_{call.provenance.value}_blocks_{risk}_risk_tool"

        # 2. Capability token must exist for this tool.
        token = self.tokens.get(call.tool)
        if not token:
            return False, f"no_token_for_{call.tool.value}"

        # 3. Scope, checked against the tool's designated argument only.
        scope_arg = cfg.get("scope_arg", DEFAULT_TOOL_CONFIG.get(call.tool.value, {}).get("scope_arg"))
        if scope_arg is None:
            return False, f"no_scope_arg_configured_for_{call.tool.value}"
        if scope_arg not in call.args:
            return False, f"scope_arg_missing_{scope_arg}"
        if not self._scope_allows(token.scope, call.args[scope_arg]):
            return False, f"scope_violation_{token.scope}"

        return True, "authorized"

    @staticmethod
    def _scope_allows(scope: str, value) -> bool:
        """Textual scope match: '*' matches anything, 'prefix*' matches by prefix,
        anything else must match exactly. (Prefix matching is textual: see the
        traversal probe in INSTRUCTIONS.md Step 4 and Exercise 4.3.)"""
        value = str(value)
        if scope == "*":
            return True
        if scope.endswith("*"):
            return value.startswith(scope[:-1])
        return value == scope


class MockMemory:
    """Memory store with provenance tracking."""

    def __init__(self):
        self.entries: List[Dict] = []

    def store(self, content: str, provenance: Provenance, metadata: Optional[Dict] = None):
        self.entries.append({
            "content": content,
            "provenance": provenance.value,
            "metadata": metadata or {},
        })

    def retrieve(self, query: str) -> List[Dict]:
        return [e for e in self.entries if query.lower() in e["content"].lower()]


class MockAgent:
    """Stand-in for the model: turns text into tool calls, then asks the mediator.

    The parser is deliberately naive (keyword + regex). It stands in for an LLM
    that will follow any instruction it reads; the security has to come from
    the mediator, not from the parser being clever.
    """

    PATH_RE = re.compile(r'[\w./\-]+\.\w+|/\w+(?:/\w+)*')
    RECIPIENT_RE = re.compile(r'send[_ ]message\s+to\s+([\w.@/\-]+)', re.IGNORECASE)
    TABLE_RE = re.compile(r'update[_ ]record\s+([\w/\-]+)', re.IGNORECASE)

    def __init__(self, mediator: PolicyMediator, memory: MockMemory):
        self.mediator = mediator
        self.memory = memory

    def parse_input(self, text: str, provenance: Provenance) -> List[ToolCall]:
        """Parse input text into tool calls, each tagged with the text's provenance."""
        calls = []
        text_lower = text.lower()

        if "read_file" in text_lower or "read file" in text_lower or text_lower.startswith("read "):
            patterns = self.PATH_RE.findall(text)
            path = patterns[0] if patterns else "README.md"
            if not path.startswith('/'):
                path = '/workspace/' + path
            calls.append(ToolCall(Tool.READ_FILE, {"path": path}, provenance, text))

        if "send_message" in text_lower or "send message" in text_lower:
            m = self.RECIPIENT_RE.search(text)
            to = m.group(1).rstrip('.,;:') if m else "<unspecified>"
            calls.append(ToolCall(Tool.SEND_MESSAGE, {"to": to, "body": "test"}, provenance, text))

        if "update_record" in text_lower or "update record" in text_lower:
            m = self.TABLE_RE.search(text)
            table = m.group(1).rstrip('.,;:') if m else "<unspecified>"
            calls.append(ToolCall(Tool.UPDATE_RECORD, {"table": table, "data": {}}, provenance, text))

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
                results.append({"tool": call.tool.value, "status": "blocked", "reason": reason,
                                "args": call.args})

        return {"input": text, "provenance": provenance.value, "results": results}


# ----------------------------------------------------------------------------
# The three agents: same parser, same mediator code, different configuration.

WILDCARD_TOKENS = {Tool.READ_FILE: "*", Tool.SEND_MESSAGE: "*", Tool.UPDATE_RECORD: "*"}
NARROW_TOKENS = {Tool.READ_FILE: "/workspace/*", Tool.SEND_MESSAGE: "internal/*", Tool.UPDATE_RECORD: "app/*"}


def _agent(agent_id: str, scopes: Dict[Tool, str], check_provenance: bool,
           tool_config: Optional[Dict] = None) -> MockAgent:
    tokens = [CapabilityToken(tool, scope, agent_id) for tool, scope in scopes.items()]
    mediator = PolicyMediator(tokens, tool_config or load_tool_config(), check_provenance)
    return MockAgent(mediator, MockMemory())


def create_baseline_agent(tool_config: Optional[Dict] = None) -> MockAgent:
    """Baseline: provenance ignored, wildcard tokens. Executes whatever it parses."""
    return _agent("baseline", WILDCARD_TOKENS, check_provenance=False, tool_config=tool_config)


def create_provenance_aware_agent(tool_config: Optional[Dict] = None) -> MockAgent:
    """Provenance-aware: untrusted content is blocked from medium/high-risk tools;
    tokens are still wildcards, so any target is in scope."""
    return _agent("prov_agent", WILDCARD_TOKENS, check_provenance=True, tool_config=tool_config)


def create_scope_bound_agent(tool_config: Optional[Dict] = None) -> MockAgent:
    """Scope-bound: the provenance rule plus narrow tokens
    (read_file /workspace/*, send_message internal/*, update_record app/*)."""
    return _agent("scope_agent", NARROW_TOKENS, check_provenance=True, tool_config=tool_config)


AGENTS = {
    "baseline": ("Unguarded Baseline", create_baseline_agent),
    "provenance": ("Provenance-Aware", create_provenance_aware_agent),
    "scope": ("Scope-Bound Mediator", create_scope_bound_agent),
}


def run_matrix(data: Dict) -> Dict[str, Dict[str, Dict[str, str]]]:
    """agent -> scenario -> tool -> executed|blocked, computed by running every agent."""
    matrix: Dict[str, Dict[str, Dict[str, str]]] = {}
    for key, (_, factory) in AGENTS.items():
        agent = factory(data["tools"])
        matrix[key] = {}
        for s in data["scenarios"]:
            r = agent.process(s["input"], Provenance(s["provenance"]))
            matrix[key][s["id"]] = {x["tool"]: x["status"] for x in r["results"]}
    return matrix


def main() -> None:
    data = json.loads(FIXTURE_PATH.read_text())
    print("=== AuthorityBound Demo ===\n")

    for key, (label, factory) in AGENTS.items():
        print(f"--- {label} ---")
        agent = factory(data["tools"])
        for scenario in data["scenarios"]:
            result = agent.process(scenario["input"], Provenance(scenario["provenance"]))
            print(f"  {scenario['id']} [{scenario['provenance']}]:")
            for r in result["results"]:
                mark = "✓" if r["status"] == "executed" else "✗"
                target = next(iter(r["args"].values()))
                print(f"    {mark} {r['tool']}({target}): {r['status']} ({r.get('reason', 'ok')})")
        print()


if __name__ == "__main__":
    main()
