"""Standardized result schema for all demos."""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Optional
import json
import subprocess
import sys


@dataclass
class ResultRecord:
    """Standardized result record for demo runs."""
    demo: str
    experiment: str
    seed: int
    commit: str
    environment: str
    command: str
    result: str  # "pass" | "fail" | "error"
    notes: str
    timestamp: str = ""
    duration_ms: int = 0
    metadata: Optional[dict] = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if self.metadata is None:
            self.metadata = {}

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, s: str) -> "ResultRecord":
        return cls(**json.loads(s))

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, path: str) -> "ResultRecord":
        with open(path) as f:
            return cls.from_json(f.read())


def write_result(
    demo: str,
    experiment: str,
    seed: int,
    result: str,
    notes: str,
    command: str = "",
    duration_ms: int = 0,
    metadata: Optional[dict] = None,
    output_dir: str = "results",
) -> ResultRecord:
    """Create and save a standardized result record."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    commit = get_git_commit()
    env = capture_environment()
    cmd = command or format_command(demo, experiment)

    record = ResultRecord(
        demo=demo,
        experiment=experiment,
        seed=seed,
        commit=commit,
        environment=env,
        command=cmd,
        result=result,
        notes=notes,
        duration_ms=duration_ms,
        metadata=metadata or {},
    )

    filename = f"{demo}_{experiment}_seed{seed}.json"
    record.save(os.path.join(output_dir, filename))
    return record


def read_results(demo: str, results_dir: str = "results") -> list[ResultRecord]:
    """Load all results for a demo."""
    import glob
    import os
    records = []
    for path in glob.glob(os.path.join(results_dir, f"{demo}_*.json")):
        try:
            records.append(ResultRecord.load(path))
        except Exception:
            pass
    return records


def get_git_commit() -> str:
    """Get current git commit or 'local'."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "local"


def capture_environment() -> str:
    """Capture Python version and OS."""
    import platform
    return f"Python {sys.version.split()[0]}, {platform.system()} {platform.release()}"


def format_command(demo: str, experiment: str) -> str:
    """Format the standard command used to run this experiment."""
    return f"make demo DEMO={demo.split('-')[-1]} EXPERIMENT={experiment}"