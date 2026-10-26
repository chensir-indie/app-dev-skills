"""Run the standalone release-evidence behavior tests in collection checks."""
import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / 'skills/app-publish-skill/tests/test_release_evidence.py'
SPEC = importlib.util.spec_from_file_location('app_publish_standalone_tests', PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def load_tests(loader, tests, pattern):
    return loader.loadTestsFromModule(MODULE)


if __name__ == '__main__':
    unittest.main()
