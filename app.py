#!/usr/bin/env python3
"""Vacancy board web app — carousel UI with analysis scores."""

import re
import os
import sys
import json
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    from config import WEB_PORT, WEB_HOST
except ImportError:
    WEB_PORT = 8080
    WEB_HOST = "0.0.0.0"
MD_FILE = os.path.join(BASE_DIR, "vacancies.md")
ANALYSES_FILE = os.path.join(BASE_DIR, "analyses.json")
CHANGELOG_FILE = os.path.join(BASE_DIR, "changelog.md")
LOG_FILE = os.path.join(BASE_DIR, "check.log")


def load_analyses():
    if os.path.exists(ANALYSES_FILE):
        with open(ANALYSES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_analyses(data: dict) -> None:
    with open(ANALYSES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_vacancies():
    if not os.path.exists(MD_FILE):
        return []
    with open(MD_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    analyses = load_analyses()
    sections = []
    current_section = None
    lines = content.split("\n")

    for line in lines:
        h2 = re.match(r"^## (.+)", line)
        if h2:
            current_section = {"name": h2.group(1).strip(), "items": []}
            sections.append(current_section)
            continue

        if current_section is None:
            continue

        m = re.match(r"^- \[(.+?)\]\((.+?)\)\s*(\*\((.+?)\)\*)?", line)
        if m:
            url = m.group(2)
            analysis = analyses.get(url, {})
            current_section["items"].append({
                "title": m.group(1),
                "url": url,
                "date": m.group(4) or "",
                "score": analysis.get("score", None),
                "summary": analysis.get("summary", ""),
                "type": analysis.get("type", ""),
                "salary": analysis.get("salary", ""),
                "remote": analysis.get("remote", ""),
                "published": analysis.get("published", ""),
                "status": analysis.get("status", ""),
            })

    return sections


def remove_vacancy(url: str) -> bool:
    with open(MD_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = [l for l in lines if url not in l]

    if len(new_lines) < len(lines):
        with open(MD_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        # Also remove from analyses
        analyses = load_analyses()
        if url in analyses:
            del analyses[url]
            save_analyses(analyses)
        return True
    return False


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/changelog")
def changelog_page():
    return send_file("changelog.html")


@app.route("/api/config")
def api_config():
    try:
        from config import PAGE_TITLE
    except ImportError:
        PAGE_TITLE = "Вакансії"
    return jsonify({"page_title": PAGE_TITLE})


@app.route("/api/last-check")
def api_last_check():
    if not os.path.exists(LOG_FILE):
        return jsonify({"last_check": None})
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find last "Starting vacancy check" line for the actual scan time
        for line in reversed(lines):
            m = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", line)
            if m:
                return jsonify({"last_check": m.group(1)})
    except Exception:
        pass
    return jsonify({"last_check": None})


@app.route("/api/changelog")
def api_changelog():
    if os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            return jsonify({"content": f.read()})
    return jsonify({"content": ""})


@app.route("/api/vacancies")
def api_vacancies():
    return jsonify(parse_vacancies())


@app.route("/api/vacancies", methods=["DELETE"])
def api_delete():
    url = request.json.get("url", "")
    if remove_vacancy(url):
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "not found"}), 404


if __name__ == "__main__":
    app.run(host=WEB_HOST, port=WEB_PORT)
