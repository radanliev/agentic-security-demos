"""
Provenance Taint Lattice module.
Defines security levels (TRUSTED_OPERATOR, INTERCEPTED, SYNTHETIC) and non-interference rules.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, Optional


class TaintTag(Enum):
    TRUSTED_OPERATOR = 0
    PROVENANCE_SYNTHETIC = 1
    TAINTED_INTERCEPTED = 2
    # Second untrusted-observation source (tool-using-agent instantiation of the
    # same guard): a tool RESULT the adversary can influence. Semantically parallel
    # to TAINTED_INTERCEPTED; the guard itself is source-agnostic (it keys on
    # "not TRUSTED_OPERATOR"), so adding a label changes no network result.
    TAINTED_TOOL_RESULT = 3


UNTRUSTED_TAGS = frozenset({TaintTag.TAINTED_INTERCEPTED, TaintTag.TAINTED_TOOL_RESULT})


@dataclass
class TaintedPayload:
    content: Any
    tag: TaintTag
    source_ip: str
    protocol: str
    metadata: Optional[Dict[str, Any]] = None

    def is_tainted(self) -> bool:
        return self.tag in UNTRUSTED_TAGS


class ProvenanceLattice:
    """Enforces information flow control on agent observation pipelines."""

    @staticmethod
    def tag_wire_payload(content: Any, src_ip: str, proto: str) -> TaintedPayload:
        """All wire traffic is tagged as TAINTED_INTERCEPTED by construction."""
        return TaintedPayload(
            content=content,
            tag=TaintTag.TAINTED_INTERCEPTED,
            source_ip=src_ip,
            protocol=proto
        )

    @staticmethod
    def tag_operator_instruction(instruction: str) -> TaintedPayload:
        """Operator instructions are tagged as TRUSTED_OPERATOR."""
        return TaintedPayload(
            content=instruction,
            tag=TaintTag.TRUSTED_OPERATOR,
            source_ip="127.0.0.1",
            protocol="LOCAL"
        )

    @staticmethod
    def validate_flow(source_tag: TaintTag, target_privilege_level: str) -> bool:
        """
        Non-interference check:
        Tainted intercepted data cannot drive PRIVILEGED actions.
        """
        if source_tag in UNTRUSTED_TAGS and target_privilege_level.upper() == "PRIVILEGED":
            return False
        return True
