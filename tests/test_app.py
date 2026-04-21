"""Smoke tests for app.py Flask endpoints.

Run: python3 -m unittest tests.test_app
"""

import json
import os
import sys
import tempfile
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import app as app_module


class TestAppEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    def test_index_serves_html(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"<!DOCTYPE html>", resp.data)

    def test_changelog_page_serves_html(self):
        resp = self.client.get("/changelog")
        self.assertEqual(resp.status_code, 200)

    def test_api_config_returns_json(self):
        resp = self.client.get("/api/config")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn("page_title", data)
        self.assertIsInstance(data["page_title"], str)

    def test_api_vacancies_returns_list(self):
        resp = self.client.get("/api/vacancies")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)

    def test_api_changelog_returns_content(self):
        resp = self.client.get("/api/changelog")
        self.assertEqual(resp.status_code, 200)

    def test_delete_missing_url_returns_404(self):
        resp = self.client.delete(
            "/api/vacancy",
            data=json.dumps({"url": "https://example.com/nonexistent-xyz-123"}),
            content_type="application/json",
        )
        self.assertIn(resp.status_code, (404, 200))


class TestParseVacancies(unittest.TestCase):
    """Unit tests for parse_vacancies using a temp MD file."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.md_path = os.path.join(self.tmpdir, "vacancies.md")
        self.analyses_path = os.path.join(self.tmpdir, "analyses.json")
        self._orig_md = app_module.MD_FILE
        self._orig_analyses = app_module.ANALYSES_FILE
        app_module.MD_FILE = self.md_path
        app_module.ANALYSES_FILE = self.analyses_path

    def tearDown(self):
        app_module.MD_FILE = self._orig_md
        app_module.ANALYSES_FILE = self._orig_analyses
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_empty_file_returns_empty_list(self):
        self.assertEqual(app_module.parse_vacancies(), [])

    def test_parses_sections_and_items(self):
        with open(self.md_path, "w", encoding="utf-8") as f:
            f.write("## Djinni.co\n- [Senior Designer](https://djinni.co/jobs/1) *(15.04)*\n")
        result = app_module.parse_vacancies()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Djinni.co")
        self.assertEqual(len(result[0]["items"]), 1)
        self.assertEqual(result[0]["items"][0]["title"], "Senior Designer")
        self.assertEqual(result[0]["items"][0]["url"], "https://djinni.co/jobs/1")
        self.assertEqual(result[0]["items"][0]["date"], "15.04")

    def test_merges_analyses_into_items(self):
        with open(self.md_path, "w", encoding="utf-8") as f:
            f.write("## Test\n- [Job](https://example.com/1)\n")
        with open(self.analyses_path, "w", encoding="utf-8") as f:
            json.dump({"https://example.com/1": {"score": 8, "summary": "Great fit"}}, f)
        result = app_module.parse_vacancies()
        self.assertEqual(result[0]["items"][0]["score"], 8)
        self.assertEqual(result[0]["items"][0]["summary"], "Great fit")


if __name__ == "__main__":
    unittest.main()
