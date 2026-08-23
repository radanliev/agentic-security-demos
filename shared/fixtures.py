"""Fixture generation utilities."""

import json
import hashlib
import random
from typing import Any, Dict, List
from pathlib import Path


def write_fixture(data: Any, path: Path, seed: int = 42) -> None:
    """Write a fixture file with deterministic formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, (dict, list)):
        content = json.dumps(data, indent=2, sort_keys=True)
    else:
        content = str(data)
    # Add seed comment for traceability
    if content.endswith("\n"):
        content = content[:-1]
    content += f"\n# seed={seed}\n"
    path.write_text(content)


def read_fixture(path: Path) -> Any:
    """Read a fixture file."""
    content = path.read_text()
    # Strip seed comment if present
    if "# seed=" in content:
        content = content.split("# seed=")[0].rstrip()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return content


def generate_canary(prefix: str = "CANARY", seed: int = 42) -> str:
    """Generate a deterministic canary string."""
    rng = random.Random(seed)
    suffix = "".join(rng.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=16))
    return f"{prefix}_{suffix}"


def generate_fake_hash(seed: int = 42) -> str:
    """Generate a deterministic fake SHA-256 hash."""
    rng = random.Random(seed)
    return "".join(rng.choices("0123456789abcdef", k=64))


def generate_fake_package_name(seed: int = 42) -> str:
    """Generate a deterministic fake package name."""
    rng = random.Random(seed)
    adjectives = ["secure", "fast", "tiny", "robust", "simple", "clean"]
    nouns = ["parser", "validator", "checker", "scanner", "analyzer", "builder"]
    return f"{rng.choice(adjectives)}-{rng.choice(nouns)}-{rng.randint(100,999)}"


def make_deterministic_dict(data: Dict[str, Any], seed: int) -> Dict[str, Any]:
    """Create a copy of dict with deterministic key ordering."""
    return {k: data[k] for k in sorted(data.keys())}