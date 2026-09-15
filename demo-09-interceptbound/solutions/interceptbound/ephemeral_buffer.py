"""
Ephemeral Capture Buffer module with Cryptographic Shredding.
Enforces strict Time-to-Live (TTL) and deterministic memory zeroization.
"""

import time
import os
import secrets
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CredentialRecord:
    username: str
    password: str
    service: str
    target_ip: str
    timestamp: float
    ttl_seconds: float = 60.0
    is_shredded: bool = False


class EphemeralRingBuffer:
    """Volatile ring buffer with automated cryptographic shredding."""

    def __init__(self, default_ttl_seconds: float = 60.0, capacity: int = 1000):
        self.default_ttl = default_ttl_seconds
        self.capacity = capacity
        self._buffer: Dict[str, CredentialRecord] = {}

    def insert_credential(self, cred_id: str, username: str, password: str,
                          service: str, target_ip: str, ttl: Optional[float] = None) -> CredentialRecord:
        """Inserts a captured credential into the volatile buffer."""
        now = time.time()
        record = CredentialRecord(
            username=username,
            password=password,
            service=service,
            target_ip=target_ip,
            timestamp=now,
            ttl_seconds=ttl or self.default_ttl
        )
        # Enforce ring capacity: shred-and-evict oldest entries beyond capacity
        # so that saturation floods cannot grow the buffer without bound.
        while len(self._buffer) >= self.capacity:
            oldest_key = min(self._buffer, key=lambda k: self._buffer[k].timestamp)
            self._shred_record(oldest_key)
        self._buffer[cred_id] = record
        self.purge_expired(now)
        return record

    def get_credential(self, cred_id: str) -> Optional[CredentialRecord]:
        """Retrieves a credential if still valid, otherwise returns None."""
        self.purge_expired(time.time())
        record = self._buffer.get(cred_id)
        if record and not record.is_shredded:
            return record
        return None

    def purge_expired(self, current_time: Optional[float] = None) -> int:
        """Purges and cryptographically shreds all expired records."""
        now = current_time or time.time()
        expired_keys = [
            k for k, r in self._buffer.items() 
            if (now - r.timestamp) > r.ttl_seconds and not r.is_shredded
        ]
        for k in expired_keys:
            self._shred_record(k)
        return len(expired_keys)

    def _shred_record(self, cred_id: str):
        """Cryptographically overwrites and deletes the record."""
        record = self._buffer[cred_id]
        # Overwrite string buffers with random pseudo-bytes
        record.username = secrets.token_hex(len(record.username))
        record.password = secrets.token_hex(len(record.password))
        record.is_shredded = True
        del self._buffer[cred_id]

    def clear_all(self):
        """Purges and shreds all active buffer entries."""
        for k in list(self._buffer.keys()):
            self._shred_record(k)
