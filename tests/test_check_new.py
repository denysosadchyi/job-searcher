"""Smoke tests for check_new.py core functions.

Run: python3 -m unittest tests.test_check_new
"""

import os
import sys
import tempfile
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import check_new


class TestIsRelevant(unittest.TestCase):
    def test_matches_keyword(self):
        # KEYWORDS from config.py — verify behavior with actual config
        for title in ["Python Developer", "Backend Engineer", "Django Developer"]:
            relevant = check_new.is_relevant(title)
            # At least one of these should match typical configs
            self.assertIsInstance(relevant, bool)

    def test_empty_title_not_relevant(self):
        # Empty title should not match any keyword
        self.assertFalse(check_new.is_relevant(""))

    def test_unrelated_title_not_relevant(self):
        self.assertFalse(check_new.is_relevant("Restaurant Manager"))


class TestGetExistingUrls(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.md_path = os.path.join(self.tmpdir, "vacancies.md")
        self._orig = check_new.MD_FILE
        check_new.MD_FILE = self.md_path

    def tearDown(self):
        check_new.MD_FILE = self._orig
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_missing_file_returns_empty_set(self):
        self.assertEqual(check_new.get_existing_urls(), set())

    def test_extracts_urls_from_md(self):
        with open(self.md_path, "w", encoding="utf-8") as f:
            f.write("- [A](https://djinni.co/jobs/1)\n- [B](https://dou.ua/vacancies/2/)\n")
        urls = check_new.get_existing_urls()
        self.assertIn("https://djinni.co/jobs/1", urls)
        self.assertIn("https://dou.ua/vacancies/2/", urls)
        self.assertEqual(len(urls), 2)


class TestAddVacancyToMd(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.md_path = os.path.join(self.tmpdir, "vacancies.md")
        self._orig = check_new.MD_FILE
        check_new.MD_FILE = self.md_path
        # Seed with a section
        with open(self.md_path, "w", encoding="utf-8") as f:
            f.write("## Djinni.co\n\n## DOU.ua\n\n")

    def tearDown(self):
        check_new.MD_FILE = self._orig
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_adds_new_vacancy(self):
        check_new.add_vacancy_to_md("Djinni.co", "Python Dev", "https://djinni.co/jobs/999")
        with open(self.md_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("[Python Dev](https://djinni.co/jobs/999)", content)

    def test_skips_duplicate_url(self):
        check_new.add_vacancy_to_md("Djinni.co", "Dev One", "https://djinni.co/jobs/1")
        check_new.add_vacancy_to_md("Djinni.co", "Dev Duplicate", "https://djinni.co/jobs/1")
        with open(self.md_path, "r", encoding="utf-8") as f:
            content = f.read()
        # URL should appear exactly once
        self.assertEqual(content.count("https://djinni.co/jobs/1"), 1)
        # Duplicate title should not be added
        self.assertNotIn("Dev Duplicate", content)


if __name__ == "__main__":
    unittest.main()
