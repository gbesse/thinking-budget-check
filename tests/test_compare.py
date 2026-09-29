import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compare import TEXT, extract_choice, summarize


class BudgetTests(unittest.TestCase):
    def test_extract(self):
        self.assertEqual(extract_choice({"answers": {"route": {"choice": "billing"}}}), "billing")

    def test_summary(self):
        cases = [{"id": "a", "expected": "a"}, {"id": "b", "expected": "b"}]
        obs = {"a": {"off": {"choice": "a", "latency_ms": 10}, "on": {"choice": "a", "latency_ms": 100}}, "b": {"off": {"choice": "a", "latency_ms": 20}, "on": {"choice": "b", "latency_ms": 200}}}
        s = summarize(cases, obs)
        self.assertEqual((s["off"]["accuracy"], s["on"]["accuracy"]), (0.5, 1))
        self.assertEqual(s["off"]["median_latency_ms"], 15)

    def test_languages(self):
        self.assertEqual(set(TEXT), {"en", "fr", "es"})


if __name__ == "__main__":
    unittest.main()
