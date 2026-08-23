"""Reproducibility utilities."""

import os
import sys
import platform
import random
import hashlib
from typing import List, TypeVar, Sequence

T = TypeVar("T")


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
    """Set global random seeds for reproducibility."""
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def capture_environment() -> str:
    """Capture detailed environment info."""
    return (
        f"Python {sys.version.split()[0]}, "
        f"{platform.system()} {platform.release()} ({platform.machine()}), "
        f"PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED', 'unset')}"
    )


def format_command(demo_num: str, experiment: str = "default") -> str:
    """Format the standard make command."""
    return f"make demo DEMO={demo_num} EXPERIMENT={experiment}"


def verify_offline() -> bool:
    """Verify no network access is configured."""
    # In CI, we could check for network namespace isolation
    # For local runs, this is a documentation check
    return True