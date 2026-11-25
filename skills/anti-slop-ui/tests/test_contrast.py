#!/usr/bin/env python3
"""Checks the contrast tool against known WCAG values and verifies every token pair in tests/contrast-pairs.txt.

Run: python3 tests/test_contrast.py
"""
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "..", "scripts", "contrast.py")
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import contrast  # noqa: E402


class KnownValues(unittest.TestCase):
    def test_black_on_white(self):
        self.assertAlmostEqual(contrast.ratio("#000", "#fff"), 21.0, places=2)

    def test_767676_is_the_aa_boundary(self):
        self.assertGreaterEqual(contrast.ratio("#767676", "#ffffff"), 4.5)
        self.assertLess(contrast.ratio("#777777", "#ffffff"), 4.5)

    def test_alpha_is_composited_over_background(self):
        self.assertAlmostEqual(contrast.ratio("rgba(0,0,0,.5)", "#ffffff"), contrast.ratio("#808080", "#ffffff"), places=1)


class TokenPairs(unittest.TestCase):
    def test_all_preset_pairs_pass_their_thresholds(self):
        p = subprocess.run([sys.executable, TOOL, "--pairs", os.path.join(HERE, "contrast-pairs.txt")],
                           stdout=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(p.returncode, 0, "\n".join(l for l in p.stdout.splitlines() if "below" in l))

    def test_tool_detects_a_known_failure(self):
        p = subprocess.run([sys.executable, TOOL, "#a1a1aa", "#ffffff"], stdout=subprocess.PIPE)
        self.assertEqual(p.returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
