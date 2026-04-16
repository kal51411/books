from pathlib import Path
import json
import tempfile
import unittest

from data_pipeline.pipeline import run


SAMPLE = """user_id,email,country,signup_ts,age,is_active
u1,ALICE@example.com,us,2025-01-01T10:00:00Z,29,true
u1,alice@example.com,US,2025-01-02T10:00:00Z,30,true
u2,bad-email,USA,not-a-ts,999,yes
u3,bob@example.com,ca,2025-01-05T09:00:00Z,,0
"""


class PipelineTests(unittest.TestCase):
    def test_run_pipeline_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            raw = tmpdir / "raw.csv"
            clean = tmpdir / "clean.csv"
            quarantine = tmpdir / "quarantine.csv"
            report = tmpdir / "report.json"
            raw.write_text(SAMPLE, encoding="utf-8")

            result = run(raw, clean, quarantine, report)
            self.assertEqual(result["rows_in"], 4)
            self.assertEqual(result["rows_clean"], 2)
            self.assertEqual(result["rows_quarantine"], 1)

            report_payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertIn("issue_counts", report_payload)
            self.assertEqual(report_payload["issue_counts"]["invalid_email"], 1)


if __name__ == "__main__":
    unittest.main()
