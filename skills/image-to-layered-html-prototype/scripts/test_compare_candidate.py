#!/usr/bin/env python3
"""Regression checks for the contractless browser candidate A/B gate."""

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from compare_candidate import compare


class CandidateComparisonTest(unittest.TestCase):
    def test_improved_roi_and_full_image_is_only_a_recommendation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, color in (("reference", "#80c0a0"),
                                ("baseline", "#e03030"),
                                ("candidate", "#82bfa0")):
                Image.new("RGB", (40, 40), color).save(root / f"{name}.png")
            report = compare(root / "reference.png", root / "baseline.png",
                             root / "candidate.png", (4, 4, 36, 36))
            self.assertEqual(report["recommendation"], "keep for further visual review")
            self.assertIn("not evaluated", report["visualAcceptance"])
            self.assertGreater(report["region"]["maeImprovement"], 0)

    def test_regression_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, color in (("reference", "#80c0a0"),
                                ("baseline", "#82bfa0"),
                                ("candidate", "#e03030")):
                Image.new("RGB", (40, 40), color).save(root / f"{name}.png")
            report = compare(root / "reference.png", root / "baseline.png",
                             root / "candidate.png", (4, 4, 36, 36))
            self.assertEqual(report["recommendation"], "inspect or reject candidate")

    def test_mismatched_dimensions_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            Image.new("RGB", (40, 40)).save(root / "reference.png")
            Image.new("RGB", (40, 40)).save(root / "baseline.png")
            Image.new("RGB", (39, 40)).save(root / "candidate.png")
            with self.assertRaisesRegex(ValueError, "identical dimensions"):
                compare(root / "reference.png", root / "baseline.png",
                        root / "candidate.png", (4, 4, 36, 36))


if __name__ == "__main__":
    unittest.main()
