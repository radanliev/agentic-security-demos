"""
Root conftest.py for agentic-security-demos.
Ensures student modules in demo directories are importable when running pytest from root.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

# Add each demo's student directory to sys.path
for demo_dir in ROOT_DIR.glob("demo-*"):
    student_dir = demo_dir / "student"
    if student_dir.is_dir() and str(student_dir) not in sys.path:
        sys.path.insert(0, str(student_dir))
