"""Reproducibility utilities."""

import os
import random
import hashlib
import socket
from typing import List, TypeVar, Sequence

from .result_schema import capture_environment, format_command  # single implementations

T = TypeVar("T")

__all__ = [
    "generate_seed",
    "deterministic_shuffle",
    "set_global_seed",
    "capture_environment",
    "format_command",
    "enforce_offline",
    "verify_offline",
]


def generate_seed(base: str = "agentic-security-demos") -> int:
    """Generate a deterministic seed from a string."""
    return int(hashlib.sha256(base.encode()).hexdigest()[:8], 16)


def deterministic_shuffle(items: Sequence[T], seed: int) -> List[T]:
    """Return a deterministically shuffled copy of items."""
    rng = random.Random(seed)
    result = list(items)
    rng.shuffle(result)
    return result


def set_global_seed(seed: int) -> None:
    """Seed ``random`` for this process.

    ``PYTHONHASHSEED`` is also exported, but only *child* processes see it: the
    running interpreter's hash seed is fixed at start-up and cannot be changed
    here. Start Python with ``PYTHONHASHSEED=<seed>`` if you need reproducible
    ``hash()`` values (the demos do not rely on them).
    """
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


_ORIGINAL_SOCKET_ATTRS: dict = {}


def _network_disabled(*args, **kwargs):
    raise RuntimeError("network access is disabled (agentic-security-demos runs offline)")


def enforce_offline() -> None:
    """Install a process-wide guard that makes any socket use raise.

    Replaces ``socket.socket``, ``socket.create_connection``,
    ``socket.getaddrinfo`` and ``socket.gethostbyname`` with a function that
    raises ``RuntimeError``. Idempotent. Call it at the top of a demo (or in a
    test fixture) to turn the "100% offline" claim into something that is
    enforced rather than promised.
    """
    if _ORIGINAL_SOCKET_ATTRS:
        return
    for name in ("socket", "create_connection", "getaddrinfo", "gethostbyname"):
        _ORIGINAL_SOCKET_ATTRS[name] = getattr(socket, name)
        setattr(socket, name, _network_disabled)


def verify_offline() -> bool:
    """Report whether the offline guard installed by ``enforce_offline`` is active.

    Returns ``False`` until ``enforce_offline()`` has been called; it never
    installs anything itself and never touches the network.
    """
    return all(
        getattr(socket, name) is _network_disabled
        for name in ("socket", "create_connection", "getaddrinfo", "gethostbyname")
    )
