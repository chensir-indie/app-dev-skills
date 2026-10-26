"""Run the standalone skill's portable evidence tests in the collection suite."""
import unittest
from pathlib import Path


def load_tests(loader, tests, pattern):
    folder = Path(__file__).resolve().parents[1] / 'skills/app-competitor-analysis/tests'
    # Nested discovery changes a loader's top-level directory. Keep the outer
    # collection discovery rooted at tests/ so later modules still load.
    return unittest.TestLoader().discover(str(folder), pattern='test_*.py', top_level_dir=str(folder))
