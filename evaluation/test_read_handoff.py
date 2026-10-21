"""Regressions for the reported missing status, wrong counts, and verbosity."""
import tempfile
from pathlib import Path
import subprocess
import unittest

from check_read_handoff import check, tracked_count


GOOD = 'Status: done\nResult: Repository read.\nEvidence/checks: files_read=15; source=git ls-files -z'


class ReadHandoffTests(unittest.TestCase):
    def test_valid_acknowledgement(self):
        self.assertEqual(check(GOOD, 15), [])

    def test_reported_wrong_counts(self):
        for wrong in (13, 14):
            with self.subTest(count=wrong):
                self.assertTrue(check(GOOD.replace('files_read=15', f'files_read={wrong}'), 15))

    def test_missing_status(self):
        self.assertTrue(check(GOOD.partition('\n')[2], 15))

    def test_long_file_list(self):
        self.assertTrue(check(GOOD + '\nREADME.md\nsrc/main.py', 15))

    def test_empty_result(self):
        self.assertTrue(check(GOOD.replace('Repository read.', ''), 15))

    def test_duplicate_field(self):
        self.assertTrue(check(GOOD + '\nStatus: done', 15))

    def test_invalid_status(self):
        self.assertTrue(check(GOOD.replace('Status: done', 'Status: probably'), 15))

    def test_conflicting_counts(self):
        self.assertTrue(check(GOOD + '; files_read=13', 15))

    def test_malformed_counts(self):
        for malformed in ('15.5', '15x', '-15', '1.5e1'):
            with self.subTest(count=malformed):
                self.assertTrue(check(GOOD.replace('files_read=15', f'files_read={malformed}'), 15))

    def test_count_uses_git_entries_not_lines_or_untracked_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            subprocess.run(['git', 'init', '-q', folder], check=True)
            for name in ('one.txt', 'two words.txt', 'three\nlines.txt'):
                (root / name).write_text('fixture', encoding='utf-8')
            subprocess.run(['git', '-C', folder, 'add', '.'], check=True)
            (root / 'untracked.txt').write_text('not in inventory', encoding='utf-8')
            self.assertEqual(tracked_count(root), 3)


if __name__ == '__main__':
    unittest.main()
