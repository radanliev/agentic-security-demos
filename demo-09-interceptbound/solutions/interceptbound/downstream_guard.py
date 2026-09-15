"""
Downstream Action Guard module for InterceptBound.
Validates proposed actions derived from intercepted observations.

Enforcement layers (in order):
  1. Provenance non-interference: tainted intercepted data cannot drive PRIVILEGED actions.
  2. Target scope + port.
  3. Action allowlist (optional): for tainted data, only allowlisted verbs (default-deny).
  4. Declassification (optional): tainted data may not drive an action toward a host
     outside the authorised sink set without explicit operator declassification.
  5. Argument provenance (optional, DEFAULT-DENY): a tainted-derived allowlisted action
     to an authorised sink may carry ONLY the structured argument fields its verb declares
     (an argument schema); any additional or free-form argument field is denied. This is a
     structural default-deny, independent of how a redirect locator is encoded
     (IPv4/IPv6/hostname/URL/encoded/split) -- consistent with the paper's thesis of
     default-denying intercepted-derived flows rather than enumerating bad ones.
  6. Legacy dangerous-verb denylist (retained as a fallback layer).
"""

from dataclasses import dataclass
from typing import Dict, Any, Tuple, Optional, Set, List
from .taint_lattice import TaintTag, ProvenanceLattice
from .scope_filter import ScopeFilter

DEFAULT_DENYLIST = ["exec", "shell", "curl", "bash", "reboot", "rm", "upload_exfil"]

# Per-verb structured argument schema: the ONLY argument keys a tainted-derived
# action of that verb may carry. Everything else is denied by default.
DEFAULT_ARG_SCHEMA: Dict[str, Set[str]] = {
    "verify_credential": {"user", "username", "password", "pass", "credential", "cred"},
    "report_status":     {"status", "code"},
    "log_observation":   {"event", "code"},
    "note":              {"code"},
    "record_finding":    {"finding", "id", "code"},
}


def _all_keys(obj):
    """Every mapping key at any depth (lower-cased), so a redirect field nested under
    a permitted key cannot slip past the structural argument schema."""
    keys = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(str(k).lower()); keys |= _all_keys(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj: keys |= _all_keys(v)
    return keys


@dataclass
class ActionProposal:
    action_name: str
    target_host: str
    target_port: int
    payload_or_args: Dict[str, Any]
    source_taint: TaintTag
    privilege_level: str = "UNPRIVILEGED"
    declassified: bool = False


class DownstreamActionGuard:
    """Mediates proposed agent tool invocations. DownstreamActionGuard(scope_filter)
    reproduces the original denylist-only behaviour; the hardening layers are opt-in."""

    def __init__(self, scope_filter: ScopeFilter,
                 action_allowlist: Optional[Set[str]] = None,
                 require_declassification: bool = False,
                 authorised_sinks: Optional[Set[str]] = None,
                 inspect_arg_provenance: bool = False,
                 arg_schema: Optional[Dict[str, Set[str]]] = None,
                 denylist: Optional[List[str]] = None):
        self.scope_filter = scope_filter
        self.action_allowlist = ({a.lower() for a in action_allowlist}
                                 if action_allowlist is not None else None)
        self.require_declassification = require_declassification
        self.authorised_sinks = set(authorised_sinks or set())
        self.inspect_arg_provenance = inspect_arg_provenance
        self.arg_schema = {k.lower(): {v.lower() for v in vs}
                           for k, vs in (arg_schema if arg_schema is not None else DEFAULT_ARG_SCHEMA).items()}
        self.denylist = [d.lower() for d in (denylist if denylist is not None else DEFAULT_DENYLIST)]
        self.executed_actions = []

    def validate_and_execute(self, proposal: ActionProposal) -> Tuple[bool, Optional[str]]:
        tainted = proposal.source_taint != TaintTag.TRUSTED_OPERATOR  # Eq.1 Trusted-only bypass; harden Synthetic too (A5 defence-in-depth)
        verb = proposal.action_name.lower()

        if not ProvenanceLattice.validate_flow(proposal.source_taint, proposal.privilege_level):
            return False, f"TAINT_VIOLATION: tainted data cannot drive {proposal.privilege_level} action {proposal.action_name}"
        if not self.scope_filter.is_ip_in_scope(proposal.target_host):
            return False, f"TARGET_OUT_OF_SCOPE: {proposal.target_host}"
        if proposal.target_port not in self.scope_filter.policy.allowed_ports:
            return False, f"PORT_NOT_ALLOWED: {proposal.target_port}"
        if self.action_allowlist is not None and tainted:
            if verb not in self.action_allowlist:
                return False, f"ACTION_NOT_ALLOWLISTED: {proposal.action_name}"
        if self.require_declassification and tainted and not proposal.declassified:
            if proposal.target_host not in self.authorised_sinks:
                return False, f"DECLASSIFICATION_REQUIRED: tainted flow to {proposal.target_host}"
        # Structural default-deny on arguments (encoding-independent, recursive).
        if self.inspect_arg_provenance and tainted and not proposal.declassified:
            schema = self.arg_schema.get(verb)
            if schema is None:
                return False, f"ARG_SCHEMA_NO_VERB: {proposal.action_name} has no declared argument schema"
            extra = sorted(k for k in _all_keys(proposal.payload_or_args) if k not in schema)
            if extra:
                return False, f"ARG_SCHEMA_VIOLATION: non-schema argument field(s) {extra}"
        if tainted and (verb in self.denylist
                        or any(v in str(proposal.payload_or_args).lower() for v in self.denylist)):
            return False, f"DANGEROUS_ACTION_BLOCKED: {proposal.action_name}"

        self.executed_actions.append(proposal)
        return True, None
