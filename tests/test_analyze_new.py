"""Smoke tests for analyze_new.py utility functions.

Run: python3 -m unittest tests.test_analyze_new
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import analyze_new


class TestIsAggregateUrl(unittest.TestCase):
    def test_linkedin_is_aggregate(self):
        self.assertTrue(analyze_new.is_aggregate_url("https://linkedin.com/jobs/search?q=designer"))

    def test_indeed_is_aggregate(self):
        self.assertTrue(analyze_new.is_aggregate_url("https://indeed.com/some-listing"))

    def test_specific_djinni_job_is_not_aggregate(self):
        self.assertFalse(analyze_new.is_aggregate_url("https://djinni.co/jobs/123456-python-dev/"))

    def test_specific_dou_vacancy_is_not_aggregate(self):
        self.assertFalse(analyze_new.is_aggregate_url("https://jobs.dou.ua/companies/acme/vacancies/789/"))

    def test_dou_search_is_aggregate(self):
        self.assertTrue(analyze_new.is_aggregate_url("https://jobs.dou.ua/vacancies/?search=Python"))


class TestTextExtractor(unittest.TestCase):
    def test_extracts_plain_text(self):
        parser = analyze_new.TextExtractor()
        parser.feed("<p>Hello <b>World</b></p>")
        self.assertIn("Hello", parser.get_text())
        self.assertIn("World", parser.get_text())

    def test_skips_script_tags(self):
        parser = analyze_new.TextExtractor()
        parser.feed("<p>Visible</p><script>alert('hidden')</script>")
        text = parser.get_text()
        self.assertIn("Visible", text)
        self.assertNotIn("alert", text)

    def test_skips_style_tags(self):
        parser = analyze_new.TextExtractor()
        parser.feed("<p>Content</p><style>body { color: red; }</style>")
        text = parser.get_text()
        self.assertIn("Content", text)
        self.assertNotIn("color: red", text)


if __name__ == "__main__":
    unittest.main()
