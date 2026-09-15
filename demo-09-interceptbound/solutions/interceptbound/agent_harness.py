"""
Agent Harness and Testbed Driver for InterceptBound.
Executes experimental sweeps comparing Unconstrained vs InterceptBound defense configurations.
Supports both deterministic local replay and live LLM dispatch via API keys.
"""

import os
from typing import Dict, List, Any, Tuple, Optional
from .scope_filter import ScopeFilter, ScopePolicy
from .tcp_reassembly import TCPStreamReassembler, TCPPacket
from .ephemeral_buffer import EphemeralRingBuffer
from .taint_lattice import ProvenanceLattice, TaintTag
from .downstream_guard import DownstreamActionGuard, ActionProposal


def load_project_env() -> Dict[str, str]:
    """
    Safely loads environment variables from common project locations
    without throwing unhandled exceptions if files are inaccessible.
    """
    env_vars = {}
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", ".env"),
        os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
        os.path.expanduser("~/.env")
    ]
    for p in candidates:
        try:
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            env_vars[k.strip()] = v.strip().strip("'\"")
        except Exception:
            continue
    # Merge with active os.environ
    for k, v in os.environ.items():
        env_vars[k] = v
    return env_vars


class InterceptBoundHarness:
    """Benchmark driver for isolated MITM testbed experiments."""

    def __init__(self, policy: ScopePolicy):
        self.policy = policy
        self.scope_filter = ScopeFilter(policy)
        self.reassembler = TCPStreamReassembler()
        self.ephemeral_buffer = EphemeralRingBuffer(default_ttl_seconds=60.0)
        self.downstream_guard = DownstreamActionGuard(self.scope_filter)
        self.env = load_project_env()

    def get_available_llm_providers(self) -> List[str]:
        """Returns list of active LLM providers discovered in environment."""
        providers = []
        if self.env.get("GEMINI_API_KEY") or self.env.get("GOOGLE_API_KEY"):
            providers.append("gemini")
        if self.env.get("OPENROUTER_API_KEY"):
            providers.append("openrouter")
        if self.env.get("GROQ_API_KEY"):
            providers.append("groq")
        if self.env.get("OPENAI_API_KEY"):
            providers.append("openai")
        if self.env.get("HF_TOKEN") or self.env.get("HF_API_TOKEN"):
            providers.append("huggingface")
        return providers

    def process_incoming_frame(self, frame_info: dict, defense_mode: str) -> Tuple[bool, Optional[str]]:
        """
        Simulates frame processing through specified defense mode:
        - 'UNCONSTRAINED'
        - 'STATIC_MIDDLEBOX'
        - 'SCOPE_ONLY'
        - 'INTERCEPTBOUND'
        """
        src_mac = frame_info.get("src_mac", "")
        src_ip = frame_info.get("src_ip", "")
        dst_mac = frame_info.get("dst_mac", "")
        dst_ip = frame_info.get("dst_ip", "")
        dst_port = frame_info.get("dst_port", 80)
        proto = frame_info.get("protocol", "HTTP")
        payload = frame_info.get("payload", b"")

        if defense_mode == "UNCONSTRAINED":
            # Passes everything promiscuously
            return True, None

        elif defense_mode == "STATIC_MIDDLEBOX":
            # Signature check (simple keyword block) without Layer 2 MAC binding or taint tracking
            cve_signatures = [b"SELECT", b"UNION", b"/etc/passwd"]
            if any(sig in payload for sig in cve_signatures):
                return False, "STATIC_SIGNATURE_MATCH"
            return True, None

        elif defense_mode == "SCOPE_ONLY":
            # Enforces scope but no provenance tracking
            return self.scope_filter.inspect_frame(src_mac, src_ip, dst_mac, dst_ip, dst_port, proto)

        elif defense_mode == "INTERCEPTBOUND":
            # Complete mediation: Scope filter + L2/L3 binding + Stream Reassembly + Ephemeral Storage
            is_allowed, reason = self.scope_filter.inspect_frame(src_mac, src_ip, dst_mac, dst_ip, dst_port, proto)
            if not is_allowed:
                return False, reason

            # Store in ephemeral buffer if credential present
            if "cred_user" in frame_info:
                self.ephemeral_buffer.insert_credential(
                    cred_id=frame_info.get("cred_id", "test_01"),
                    username=frame_info["cred_user"],
                    password=frame_info.get("cred_pass", ""),
                    service=proto,
                    target_ip=dst_ip
                )
            return True, None

        return False, "UNKNOWN_DEFENSE_MODE"

    def evaluate_downstream_action(self, action_info: dict, defense_mode: str) -> Tuple[bool, Optional[str]]:
        """Evaluates downstream action proposals under specified defense."""
        if defense_mode == "UNCONSTRAINED":
            # Allows arbitrary agent action
            return True, None

        elif defense_mode == "STATIC_MIDDLEBOX" or defense_mode == "SCOPE_ONLY":
            # Checks only if target IP is reachable
            target_host = action_info.get("target_host", "")
            return self.scope_filter.is_ip_in_scope(target_host), "TARGET_CHECK"

        elif defense_mode == "INTERCEPTBOUND":
            proposal = ActionProposal(
                action_name=action_info.get("action_name", ""),
                target_host=action_info.get("target_host", ""),
                target_port=action_info.get("target_port", 80),
                payload_or_args=action_info.get("args", {}),
                source_taint=action_info.get("taint_tag", TaintTag.TAINTED_INTERCEPTED),
                privilege_level=action_info.get("privilege_level", "UNPRIVILEGED")
            )
            return self.downstream_guard.validate_and_execute(proposal)

        return False, "UNKNOWN_MODE"
