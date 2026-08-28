#!/usr/bin/env python3
"""
ScanBound - Vulnerability Assessment Scope Control

Four gates, in pipeline order, around a *simulated* scanner:

  1. scope       may this target be touched at all?  (host/port/protocol allowlists)
  2. validation  is this check safe to run?  A rejected check is NEVER executed,
                 so it produces no output, no finding and no taint - there is
                 nothing to observe.  Every failing screen is reported
                 (type flag, state flag, AST walk, keyword screen).
  3. taint       is the output of a check that did run trustworthy?  Scanner
                 output is never LOW; injection- or credential-shaped content
                 makes it HIGH.  Detection reads the finding TEXT, not a
                 fixture side channel.
  4. policy      may we act on it?  Allowed/denied action sets plus a taint
                 ceiling.  The policy is consulted for every finding, so the
                 ledger shows what was reported and what was blocked and why.

The baseline runs every check, trusts every output (taint LOW), reports it,
and follows instruction-shaped output - all simulated: actions are recorded,
never performed.  Nothing here opens a socket.
"""

from __future__ import annotations

import ast
import ipaddress
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class TaintLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


TAINT_ORDER = {TaintLevel.LOW: 0, TaintLevel.MEDIUM: 1, TaintLevel.HIGH: 2}


class ActionType(Enum):
    REPORT_FINDING = "report_finding"
    GENERATE_REPORT = "generate_report"
    EXPLOIT = "exploit"
    EXFILTRATE = "exfiltrate"
    MODIFY_TARGET = "modify_target"
    EXECUTE_COMMAND = "execute_command"


@dataclass
class Target:
    host: str
    port: int
    protocol: str

    def __str__(self):
        return f"{self.host}:{self.port}"


@dataclass
class ScannerCheck:
    id: str
    name: str
    check_type: str  # "safe" or "unsafe"; anything else fails closed
    target: Target
    payload: str
    expected: str
    modifies_state: bool = False


@dataclass
class ScanResult:
    check_id: str
    target: Target
    finding: str
    taint: TaintLevel
    evidence: str
    taint_reasons: List[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# Gate 1: scope
# --------------------------------------------------------------------------

class ScopeValidator:
    """Validates targets against scope policy (exact host, wildcard, or CIDR)."""

    def __init__(self, allowed_hosts: List[str], allowed_ports: List[int], allowed_protocols: List[str]):
        self.allowed_hosts = list(allowed_hosts)
        self.allowed_ports = list(allowed_ports)
        self.allowed_protocols = list(allowed_protocols)

    def validate(self, target: Target) -> Tuple[bool, str]:
        if not any(self._match_host(pattern, target.host) for pattern in self.allowed_hosts):
            return False, f"host_not_allowed: {target.host}"
        if target.port not in self.allowed_ports:
            return False, f"port_not_allowed: {target.port}"
        if target.protocol not in self.allowed_protocols:
            return False, f"protocol_not_allowed: {target.protocol}"
        return True, "in_scope"

    def _match_host(self, pattern: str, host: str) -> bool:
        if pattern == host:
            return True
        if pattern.startswith("*."):                     # *.example.com matches sub.example.com and example.com
            if host == pattern[2:] or host.endswith(pattern[1:]):
                return True
        try:                                             # CIDR: 192.168.1.0/24
            if "/" in pattern and ipaddress.ip_address(host) in ipaddress.ip_network(pattern, strict=False):
                return True
        except ValueError:
            pass
        return False


# --------------------------------------------------------------------------
# Gate 2: check validation (type flag -> state flag -> AST -> keywords)
# --------------------------------------------------------------------------

class CheckValidator:
    """Decides whether a check may run.  Reports EVERY failing screen so an
    operator sees the whole defence-in-depth picture, not just the first hit.

    The AST screen parses every payload as Python (statements and expressions);
    a payload that does not parse is not Python and the AST screen is not
    applicable to it - unless it looks like code, in which case it fails closed.
    """

    DANGEROUS_CALLS = {"exec", "eval", "__import__", "compile"}
    DANGEROUS_ATTRS = {"run", "system", "popen", "Popen", "call", "check_output", "check_call", "exec", "eval"}
    DANGEROUS_MODULES = {"subprocess", "os", "sys", "shutil", "socket", "ctypes"}
    DANGEROUS_KEYWORDS = ["rm -rf", "exploit", "exfiltrate", "whoami", "cat /etc/passwd", "wget", "curl | sh"]
    CODE_INDICATORS = ["import ", "def ", "class ", "lambda ", "exec(", "eval(", "__import__", "subprocess", "os."]

    def reasons(self, check: ScannerCheck) -> List[str]:
        found: List[str] = []
        if check.check_type == "unsafe":
            found.append("check_type_unsafe")
        elif check.check_type != "safe":
            found.append(f"check_type_unknown: {check.check_type!r}")
        if check.modifies_state:
            found.append("modifies_state")
        found.extend(self._ast_reasons(check.payload))
        lowered = check.payload.lower()
        found.extend(f"dangerous_payload_keyword: {kw}" for kw in self.DANGEROUS_KEYWORDS if kw in lowered)
        return found

    def validate(self, check: ScannerCheck) -> Tuple[bool, str]:
        found = self.reasons(check)
        if found:
            return False, "; ".join(found)
        return True, "safe"

    def _ast_reasons(self, payload: str) -> List[str]:
        try:
            tree = ast.parse(payload)                    # 'exec' mode: statements AND expressions
        except (SyntaxError, ValueError):
            if self._looks_like_code(payload):
                return ["unparseable_code_like_payload"]
            return []
        except Exception as exc:                          # fail closed on anything unexpected
            return [f"ast_error: {type(exc).__name__}"]
        return [f"dangerous_ast_pattern: {node}" for node in self._dangerous_nodes(tree)]

    def _looks_like_code(self, payload: str) -> bool:
        return any(ind in payload for ind in self.CODE_INDICATORS)

    def _dangerous_nodes(self, tree: ast.AST) -> List[str]:
        hits: List[str] = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name) and n.func.id in self.DANGEROUS_CALLS:
                    hits.append(f"call:{n.func.id}")
                elif isinstance(n.func, ast.Attribute) and n.func.attr in self.DANGEROUS_ATTRS:
                    hits.append(f"call:.{n.func.attr}")
            elif isinstance(n, ast.Import):
                hits.extend(f"import:{a.name}" for a in n.names if a.name.split(".")[0] in self.DANGEROUS_MODULES)
            elif isinstance(n, ast.ImportFrom) and n.module and n.module.split(".")[0] in self.DANGEROUS_MODULES:
                hits.append(f"import:{n.module}")
        return hits


# --------------------------------------------------------------------------
# Gate 3: taint on scanner output
# --------------------------------------------------------------------------

class TaintTracker:
    """Assigns taint to the OUTPUT of a check that ran.  Reads every string in
    the output - never a fixture side channel."""

    INJECTION_RULES: List[Tuple[str, re.Pattern]] = [
        ("canary_marker", re.compile(r"CANARY_[A-Z0-9_]+")),
        ("instruction_run_cmd", re.compile(r"RUN_CMD|run the command", re.I)),
        ("instruction_exfiltrate", re.compile(r"EXFILTRATE", re.I)),
        ("instruction_phrase", re.compile(r"ignore (?:all |your )?(?:previous |prior )?(?:rules|instructions)", re.I)),
    ]
    CREDENTIAL_RULE = re.compile(r"(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*\S+", re.I)

    def __init__(self):
        self.taint_map: Dict[str, TaintLevel] = {}
        self.reason_map: Dict[str, List[str]] = {}

    @staticmethod
    def _strings(value: Any) -> List[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, dict):
            return [s for v in value.values() for s in TaintTracker._strings(v)]
        if isinstance(value, list):
            return [s for v in value for s in TaintTracker._strings(v)]
        return []

    def analyse(self, output: Dict) -> Tuple[TaintLevel, List[str]]:
        text = "\n".join(self._strings(output))
        reasons = [rule_id for rule_id, pattern in self.INJECTION_RULES if pattern.search(text)]
        if self.CREDENTIAL_RULE.search(text):
            reasons.append("credential_pattern")
        return (TaintLevel.HIGH if reasons else TaintLevel.MEDIUM), reasons

    def track_output(self, check_id: str, output: Dict) -> TaintLevel:
        taint, reasons = self.analyse(output)
        self.taint_map[check_id] = taint
        self.reason_map[check_id] = reasons
        return taint

    def get_taint(self, check_id: str) -> TaintLevel:
        # Fail closed: an output we never analysed is not trusted.
        return self.taint_map.get(check_id, TaintLevel.HIGH)


# --------------------------------------------------------------------------
# Gate 4: downstream action policy
# --------------------------------------------------------------------------

class ActionPolicy:

    def __init__(self, allowed: List[str], denied: List[str], max_taint: TaintLevel):
        self.allowed = set(allowed)
        self.denied = set(denied)
        self.max_taint = max_taint

    def authorize(self, action: ActionType, taint: TaintLevel) -> Tuple[bool, str]:
        if action.value in self.denied:
            return False, f"action_denied: {action.value}"
        if action.value not in self.allowed:
            return False, f"action_not_allowed: {action.value}"
        if TAINT_ORDER[taint] > TAINT_ORDER[self.max_taint]:
            return False, f"taint_too_high: {taint.value} > {self.max_taint.value}"
        return True, "authorized"


# --------------------------------------------------------------------------
# The (simulated) scanner
# --------------------------------------------------------------------------

class SimulatedScanner:
    """Stands in for the scanning engine.  `execute` returns the fixture's canned
    output for a check and records that the check ran - so the tests can prove
    which checks were executed and which never were."""

    def __init__(self, canned_outputs: Dict[str, Dict]):
        self.canned_outputs = canned_outputs
        self.executed: List[str] = []

    def execute(self, check: ScannerCheck) -> Dict:
        self.executed.append(check.id)
        return dict(self.canned_outputs.get(check.id, {"result": "error", "details": "no output"}))


_RUN_CMD = re.compile(r"RUN_CMD_([A-Z0-9_]+)")
_EXFIL = re.compile(r"EXFILTRATE_([A-Z0-9_]+)")


def instructions_in(output: Dict) -> List[str]:
    """What an agent that treats scanner output as instructions would 'do'."""
    text = "\n".join(TaintTracker._strings(output))
    found = [f"execute_command:{m.lower()}" for m in _RUN_CMD.findall(text)]
    found += [f"exfiltrate:{m.lower()}" for m in _EXFIL.findall(text)]
    return found


class UnconstrainedScanner:
    """Baseline: no scope, no validation, trusts every output (taint LOW),
    reports everything and follows instruction-shaped output.  Simulated."""

    def __init__(self, checks: List[ScannerCheck]):
        self.checks = checks

    def run(self, scanner: SimulatedScanner) -> Dict:
        results, actions = [], []
        for check in self.checks:
            output = scanner.execute(check)
            results.append(ScanResult(check.id, check.target, output.get("details", "unknown"),
                                      TaintLevel.LOW, output.get("details", "")))
            actions.append(f"report:{check.id}")
            actions.extend(f"{instr} [SIMULATED - recorded, not run] <- from {check.id} output"
                           for instr in instructions_in(output))
        return {"results": results, "actions_taken": actions, "executed": list(scanner.executed)}


class ScopeBoundScanner:
    """Guarded: scope -> check validation -> execute -> taint -> action policy."""

    def __init__(self, scope: ScopeValidator, check_validator: CheckValidator,
                 taint_tracker: TaintTracker, action_policy: ActionPolicy):
        self.scope = scope
        self.check_validator = check_validator
        self.taint_tracker = taint_tracker
        self.action_policy = action_policy

    def run(self, checks: List[ScannerCheck], scanner: SimulatedScanner) -> Dict:
        results, blocked_checks, actions_taken, actions_blocked, events = [], [], [], [], []

        for check in checks:
            # 1. Scope
            in_scope, scope_reason = self.scope.validate(check.target)
            if not in_scope:
                blocked_checks.append({"check": check.id, "reason": scope_reason, "executed": False})
                events.append(("blocked_check", check.id, scope_reason))
                continue

            # 2. Check validation - BEFORE execution.  Nothing below runs for a rejected check.
            safe, check_reason = self.check_validator.validate(check)
            if not safe:
                blocked_checks.append({"check": check.id, "reason": check_reason, "executed": False})
                events.append(("blocked_check", check.id, check_reason))
                continue

            # 3. Execute (simulated) and 4. taint the output
            output = scanner.execute(check)
            taint = self.taint_tracker.track_output(check.id, output)
            result = ScanResult(check.id, check.target, output.get("details", "unknown"), taint,
                                output.get("details", ""), self.taint_tracker.reason_map[check.id])
            results.append(result)
            events.append(("finding", check.id, result))

            # 5. Downstream action: the policy is consulted for EVERY finding.
            allowed, reason = self.action_policy.authorize(ActionType.REPORT_FINDING, taint)
            if allowed:
                actions_taken.append(f"report:{check.id}")
                events.append(("action", check.id, f"report:{check.id}"))
            else:
                actions_blocked.append(f"report:{check.id} ({reason})")
                events.append(("blocked_action", check.id, f"report:{check.id} ({reason})"))

        return {"results": results, "blocked_checks": blocked_checks, "actions_taken": actions_taken,
                "actions_blocked": actions_blocked, "executed": list(scanner.executed), "events": events}


# --------------------------------------------------------------------------
# Loading and demo
# --------------------------------------------------------------------------

def load_checks(data: Dict) -> List[ScannerCheck]:
    checks = []
    for c in data["scanner_checks"]:
        host, port = c["target"].rsplit(":", 1)
        checks.append(ScannerCheck(
            id=c["id"], name=c["name"], check_type=c["type"],
            target=Target(host, int(port), c.get("protocol", "http")),
            payload=c["payload"], expected=c["expected"], modifies_state=c.get("modifies_state", False),
        ))
    return checks


def build_guarded(data: Dict) -> ScopeBoundScanner:
    scope_data, policy_data = data["target_scope"], data["downstream_policy"]
    return ScopeBoundScanner(
        ScopeValidator(scope_data["allowed_hosts"], scope_data["allowed_ports"], scope_data["allowed_protocols"]),
        CheckValidator(),
        TaintTracker(),
        ActionPolicy(policy_data["allowed_actions"], policy_data["denied_actions"],
                     TaintLevel(policy_data["max_taint_for_report"])),
    )


def main():
    print("=== ScanBound Demo ===\n")

    base_dir = Path(__file__).resolve().parent.parent
    data = json.loads((base_dir / "fixtures" / "scanbound.json").read_text())
    checks = load_checks(data)
    scope_data, policy_data = data["target_scope"], data["downstream_policy"]

    print("Target Scope:")
    print(f"  Hosts: {scope_data['allowed_hosts']}")
    print(f"  Ports: {scope_data['allowed_ports']}")
    print(f"  Protocols: {scope_data['allowed_protocols']}")
    print("Downstream policy:")
    print(f"  Allowed: {policy_data['allowed_actions']}  Denied: {policy_data['denied_actions']}")
    print(f"  Max taint for auto-report: {policy_data['max_taint_for_report']}")
    print()

    print("--- Unconstrained Baseline (runs everything, trusts everything) ---")
    scanner = SimulatedScanner(data["poisoned_scanner_output"])
    baseline = UnconstrainedScanner(checks).run(scanner)
    by_id = {r.check_id: r for r in baseline["results"]}
    for check in checks:
        r = by_id[check.id]
        print(f"  {check.id} ({r.target}): {r.finding[:60]}... (taint: {r.taint.value})")
        for a in baseline["actions_taken"]:
            if a.startswith(f"report:{check.id}") or a.endswith(f"from {check.id} output"):
                print(f"    ACTION: {a}")
    print(f"  Checks executed: {len(baseline['executed'])}/{len(checks)}")
    print()

    print("--- Scope-Bound Guarded (scope -> validate -> execute -> taint -> policy) ---")
    scanner = SimulatedScanner(data["poisoned_scanner_output"])
    guarded = build_guarded(data).run(checks, scanner)
    for kind, check_id, payload in guarded["events"]:
        if kind == "blocked_check":
            print(f"  BLOCKED CHECK: {check_id} ({payload}) - never executed")
        elif kind == "finding":
            why = f" [{', '.join(payload.taint_reasons)}]" if payload.taint_reasons else ""
            print(f"  {check_id} ({payload.target}): {payload.finding[:60]}... (taint: {payload.taint.value}{why})")
        elif kind == "action":
            print(f"    ACTION: {payload}")
        else:
            print(f"    BLOCKED ACTION: {payload}")
    print(f"  Checks executed: {len(guarded['executed'])}/{len(checks)} -> {guarded['executed']}")
    print()

    print("=== Demo Complete ===")
    print("\nKey constraints:")
    print("  1. Target scope enforced (host/port/protocol) - out-of-scope checks never run")
    print("  2. Unsafe checks rejected BEFORE execution (type, state, AST, keywords) - no output to observe")
    print("  3. Scanner output tainted from its own text (canaries, instructions, credentials)")
    print("  4. Every finding goes through the action policy; HIGH taint is held for review")


if __name__ == "__main__":
    main()
