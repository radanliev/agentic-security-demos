"""Shared utilities for agentic-security-demos."""

from .result_schema import ResultRecord, write_result, read_results
from .reproducibility import capture_environment, format_command, generate_seed, deterministic_shuffle, set_global_seed, enforce_offline, verify_offline
from .anonymize import Anonymizer, DeidReport, pseudonym, redact_record
from .fixtures import write_fixture, read_fixture, generate_canary, generate_fake_hash, generate_fake_package_name, make_deterministic_dict

__all__ = [
    "ResultRecord",
    "write_result",
    "read_results",
    "capture_environment",
    "format_command",
    "generate_seed",
    "deterministic_shuffle",
    "set_global_seed",
    "enforce_offline",
    "verify_offline",
    "write_fixture",
    "read_fixture",
    "generate_canary",
    "generate_fake_hash",
    "generate_fake_package_name",
    "make_deterministic_dict",
    "Anonymizer",
    "DeidReport",
    "pseudonym",
    "redact_record",
]