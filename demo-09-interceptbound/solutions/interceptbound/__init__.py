"""
InterceptBound: Scope- and Provenance-Bounded Autonomous Network Interception.
ESORICS 2027 Implementation.
"""

from .scope_filter import ScopeFilter, ScopePolicy
from .tcp_reassembly import TCPStreamReassembler, TCPPacket
from .ephemeral_buffer import EphemeralRingBuffer, CredentialRecord
from .taint_lattice import TaintTag, ProvenanceLattice, TaintedPayload
from .downstream_guard import DownstreamActionGuard, ActionProposal
from .agent_harness import InterceptBoundHarness

__all__ = [
    "ScopeFilter",
    "ScopePolicy",
    "TCPStreamReassembler",
    "TCPPacket",
    "EphemeralRingBuffer",
    "CredentialRecord",
    "TaintTag",
    "ProvenanceLattice",
    "TaintedPayload",
    "DownstreamActionGuard",
    "ActionProposal",
    "InterceptBoundHarness"
]
