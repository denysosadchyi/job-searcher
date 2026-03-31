#!/usr/bin/env python3
"""
Initial setup script — run once after editing config.py.
Generates profile.md, vacancies.md, and optionally sets up cron + systemd.
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from config import (
    PROFILE, TARGET, NOT_INTERESTED, FIT_CRITERIA,
    KEY_EXPERIENCE, SEARCH_KEYWORDS, SOURCES, GROQ_API_KEY,
    WEB_PORT, PAGE_TITLE
)


def generate_profile():
    """Generate profile.md from config."""
    lines = [
        f"# {PROFILE['name']} — Vacancy Analysis Profile\n",
        "## Target",
    ]
    for t in TARGET:
        lines.append(f"- {t}")

    lines.append(f"- Salary: ${PROFILE['salary_min']}–{PROFILE['salary_max']}+/month")
    lines.append("")
    lines.append("## Not interested")
    for n in NOT_INTERESTED:
        lines.append(f"- {n}")

    lines.append("")
    lines.append("## Fit criteria")
    lines.append(FIT_CRITERIA.strip())

    lines.append("")
    lines.append("## Key experience for matching")
    for k in KEY_EXPERIENCE:
        lines.append(f"- {k}")

    lines.append("")
    lines.append("## Scoring guide")
    lines.append(f"- 8-10: Perfect match — product company, right domain, ${PROFILE['salary_min']}+, remote")
    lines.append("- 6-7: Good potential — mostly matches with minor gaps")
    lines.append("- 4-5: Worth looking at — some red flags but interesting aspects")
    lines.append("- 1-3: Skip — agencies, wrong level, low salary, office-only")

    path = os.path.join(BASE_DIR, "profile.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[OK] Generated profile.md")


def generate_vacancies_md():
    """Generate initial vacancies.md."""
    path = os.path.join(BASE_DIR, "vacancies.md")
    if os.path.exists(path):
        print(f"[SKIP] vacancies.md already exists")
        return

    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [
        f"# {PROFILE['title']} — Vacancies",
        "",
        f"Дата пошуку: {today}",
        f"Оновлено: {today}",
        "",
        "---",
        "",
    ]

    # Map config names to section names used by check_new.py
    SECTION_MAP = {"Djinni": "Djinni.co", "DOU": "DOU.ua"}

    for name, cfg in SOURCES.items():
        if cfg["enabled"]:
            section_name = SECTION_MAP.get(name, name)
            lines.append(f"## {section_name}")
            lines.append("")
            lines.append(f"- [All vacancies]({cfg['url']})")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Search URLs")
    lines.append("")
    for name, cfg in SOURCES.items():
        if cfg["enabled"]:
            lines.append(f"- {name}: {cfg['url']}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[OK] Generated vacancies.md")


def generate_analyses_json():
    """Create empty analyses.json if not exists."""
    path = os.path.join(BASE_DIR, "analyses.json")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("{}")
        print(f"[OK] Created analyses.json")


def check_dependencies():
    """Check and install required Python packages."""
    try:
        import flask
        print("[OK] Flask already installed")
    except ImportError:
        print("[...] Installing Flask...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"], check=True)
        print("[OK] Flask installed")


def setup_systemd():
    """Offer to set up systemd service for the web server."""
    ans = input("\nSet up web server as systemd service (auto-start on boot)? [y/N]: ").strip().lower()
    if ans != 'y':
        return

    user = os.environ.get("USER", "nobody")
    service = f"""[Unit]
Description=Job Search Vacancy Board
After=network.target

[Service]
Type=simple
User={user}
WorkingDirectory={BASE_DIR}
ExecStart={sys.executable} {os.path.join(BASE_DIR, 'app.py')}
Restart=always
RestartSec=5
Environment=GROQ_API_KEY={GROQ_API_KEY}

[Install]
WantedBy=multi-user.target
"""
    service_path = "/etc/systemd/system/job-search.service"
    try:
        with open("/tmp/job-search.service", "w") as f:
            f.write(service)
        subprocess.run(["sudo", "cp", "/tmp/job-search.service", service_path], check=True)
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "job-search"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "job-search"], check=True)
        print(f"[OK] Web server running on port {WEB_PORT}")
        print(f"     Open http://localhost:{WEB_PORT} in your browser")
    except Exception as e:
        print(f"[ERROR] Failed to set up systemd: {e}")
        print(f"        You can start manually: python3 app.py")


def setup_cron():
    """Offer to set up cron for periodic vacancy checking."""
    ans = input("\nSet up cron to check for new vacancies every 2 hours? [y/N]: ").strip().lower()
    if ans != 'y':
        return

    cron_line = f"23 */2 * * * GROQ_API_KEY={GROQ_API_KEY} {sys.executable} {os.path.join(BASE_DIR, 'check_new.py')} >> {os.path.join(BASE_DIR, 'check.log')} 2>&1"

    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ""

        if "check_new.py" in existing:
            print("[SKIP] Cron already set up")
            return

        new_cron = existing.rstrip() + "\n" + cron_line + "\n"
        proc = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        proc.communicate(input=new_cron)
        print("[OK] Cron job added — checking every 2 hours")
    except Exception as e:
        print(f"[ERROR] Failed to set up cron: {e}")
        print(f"        Add manually: crontab -e")
        print(f"        {cron_line}")


def main():
    print("=" * 50)
    print(f"  Job Search Setup for {PROFILE['name']}")
    print("=" * 50)
    print()

    if not PROFILE["name"] or PROFILE["name"] == "Your Name":
        print("[!] Please edit config.py first with your details!")
        print(f"    nano {os.path.join(BASE_DIR, 'config.py')}")
        sys.exit(1)

    check_dependencies()
    generate_profile()
    generate_vacancies_md()
    generate_analyses_json()

    if not GROQ_API_KEY:
        print("\n[!] No Groq API key in config.py")
        print("    Get a free key at: https://console.groq.com")
        print("    Vacancies will be collected but NOT analyzed until you add the key.")

    setup_systemd()
    setup_cron()

    print("\n" + "=" * 50)
    print("  Setup complete!")
    print("=" * 50)
    print(f"\n  Web UI: http://localhost:{WEB_PORT}")
    print(f"  First run: python3 check_new.py")
    print(f"  Analyze: python3 analyze_new.py")


if __name__ == "__main__":
    main()
