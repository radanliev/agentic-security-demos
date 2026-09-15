"""
Scope Filter module for InterceptBound.
Enforces Layer 2 (MAC), Layer 3 (IP/CIDR), and Layer 4/7 (Port/Protocol) boundaries.
"""

import ipaddress
from dataclasses import dataclass, field
from typing import Dict, Set, Optional, Tuple


@dataclass(frozen=True)
class ScopePolicy:
    """Formal Scope Policy definition P_scope."""
    allowed_cidrs: Set[str] = field(default_factory=set)
    mac_ip_bindings: Dict[str, str] = field(default_factory=dict) # IP -> MAC
    allowed_ports: Set[int] = field(default_factory=lambda: {80, 21, 23, 25, 110, 143})
    allowed_protocols: Set[str] = field(default_factory=lambda: {"HTTP", "FTP", "TELNET", "SMTP", "IMAP"})
    max_interception_window_sec: float = 300.0
    activation_epoch: Optional[float] = None  # None => window not enforced


class ScopeFilter:
    """In-kernel / packet-level Scope Filter."""

    def __init__(self, policy: ScopePolicy):
        self.policy = policy
        self._parsed_networks = [ipaddress.ip_network(cidr, strict=False) for cidr in policy.allowed_cidrs]

    def is_ip_in_scope(self, ip_str: str) -> bool:
        """Verifies if an IP belongs to the authorized CIDR subnets."""
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            return any(ip_obj in net for net in self._parsed_networks)
        except (ValueError, TypeError):
            return False  # fail-closed on malformed target (list/NUL/Unicode/hostname)

    def is_mac_bound(self, ip_str: str, mac_str: str) -> bool:
        """Verifies that the Layer 2 MAC matches the authorized IP binding."""
        if not self.policy.mac_ip_bindings:
            return True
        expected_mac = self.policy.mac_ip_bindings.get(ip_str)
        if expected_mac is None:
            return False
        return expected_mac.lower() == mac_str.lower()

    def inspect_frame(self, src_mac: str, src_ip: str, dst_mac: str, dst_ip: str,
                      dst_port: int, protocol_name: str,
                      timestamp: Optional[float] = None) -> Tuple[bool, Optional[str]]:
        """
        Inspects an incoming frame.
        Returns (is_allowed, drop_reason).
        When policy.activation_epoch and a frame timestamp are provided, the
        authorized interception window T_window of P_scope is enforced.
        """
        # 0. Authorized interception window (T_window)
        if self.policy.activation_epoch is not None and timestamp is not None:
            if timestamp - self.policy.activation_epoch > self.policy.max_interception_window_sec:
                return False, f"INTERCEPTION_WINDOW_EXCEEDED: limit {self.policy.max_interception_window_sec}s"

        # 1. Source IP Scope
        if not self.is_ip_in_scope(src_ip):
            return False, f"SRC_IP_OUT_OF_SCOPE: {src_ip}"

        # 2. Destination IP Scope
        if not self.is_ip_in_scope(dst_ip):
            return False, f"DST_IP_OUT_OF_SCOPE: {dst_ip}"

        # 3. Source MAC binding
        if not self.is_mac_bound(src_ip, src_mac):
            return False, f"SRC_MAC_MISMATCH: {src_ip} vs {src_mac}"

        # 4. Port and Protocol validation
        if dst_port not in self.policy.allowed_ports:
            return False, f"PORT_NOT_ALLOWED: {dst_port}"

        if protocol_name.upper() not in self.policy.allowed_protocols:
            return False, f"PROTOCOL_NOT_ALLOWED: {protocol_name}"

        return True, None
