#!/usr/bin/env python3
"""
scraper.py — Scraper skeleton for HK seminary theology courses
==============================================================
This script provides per-school scraper stubs for the main Hong Kong
seminary institutions.  Each scraper fetches the school's course listing
page(s), parses the HTML, and returns a list of course dicts that conform
to the shared schema used by data/courses.json.

Usage
-----
    # Scrape all schools and write to data/courses.json
    python scraper/scraper.py

    # Scrape a single school
    python scraper/scraper.py --school abs

    # Dry-run (print JSON to stdout instead of writing)
    python scraper/scraper.py --dry-run

Requirements
------------
    pip install requests beautifulsoup4 lxml

Course schema (matches data/courses.json)
-----------------------------------------
{
    "id":          str,   # e.g. "ABS-001"
    "title_en":    str,
    "title_zh":    str,
    "school":      str,   # English full name
    "school_zh":   str,   # Chinese full name
    "school_url":  str,
    "level":       str,   # "seminar" | "entry" | "credit" | "degree"
    "themes":      list[str],
    "bible_books": list[str],
    "description": str,
    "credits":     int,   # 0 for non-credit
    "url":         str,   # Direct link to the course page
    "semester":    str,   # e.g. "2024 Fall"
}
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit(
        "Missing dependencies.  Run:  pip install requests beautifulsoup4 lxml"
    )

# ── Configuration ─────────────────────────────────────────────────────────────

DATA_FILE = Path(__file__).parent.parent / "data" / "courses.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; HKSeminaryCatalogueScraper/1.0; "
        "+https://github.com/hktlc/courses)"
    )
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)


# ── Shared utilities ───────────────────────────────────────────────────────────

def fetch(url: str, timeout: int = 15) -> BeautifulSoup:
    """Fetch a URL and return a BeautifulSoup object."""
    log.info("GET %s", url)
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")


def polite_sleep(seconds: float = 1.5) -> None:
    """Sleep between requests to be a polite scraper."""
    time.sleep(seconds)


DEGREE_KEYWORDS = (
    "doctor", "phd", "ph.d", "d.min", "d.th",
    "master", "m.div", "th.m", "m.a", "b.th",
    "bachelor", "licentiate", "diploma",
)
SEMINAR_KEYWORDS = ("seminar", "workshop", "retreat", "short course", "非學分", "研討")
ENTRY_KEYWORDS = ("introduction", "introductory", "survey", "overview", "入門", "概論")


def detect_level(text: str) -> str:
    """
    Heuristically map free-text level indicators to the catalogue levels.

    Returns one of: "seminar", "entry", "credit", "degree"
    """
    text_lower = text.lower()
    if any(k in text_lower for k in DEGREE_KEYWORDS):
        return "degree"
    if any(k in text_lower for k in SEMINAR_KEYWORDS):
        return "seminar"
    if any(k in text_lower for k in ENTRY_KEYWORDS):
        return "entry"
    return "credit"


def extract_credits(text: str) -> int:
    """
    Extract numeric credit count from a string such as "3 credits" or "學分: 3".
    Returns 0 if no credits are found.
    """
    import re
    match = re.search(r"(\d+)\s*credit", text, re.IGNORECASE)
    if not match:
        match = re.search(r"學分[：:]\s*(\d+)", text)
    return int(match.group(1)) if match else 0


# ── Per-school scrapers ────────────────────────────────────────────────────────

def scrape_abs() -> list[dict[str, Any]]:
    """
    Alliance Bible Seminary (建道神學院)
    https://www.abs.edu.hk

    NOTE: The live website structure must be inspected before activating this
    scraper.  The selectors below are illustrative placeholders.
    """
    BASE = "https://www.abs.edu.hk"
    courses: list[dict[str, Any]] = []
    counter = 1

    # Example: iterate over a courses listing page
    # soup = fetch(f"{BASE}/courses")
    # for item in soup.select(".course-item"):
    #     title_en = item.select_one(".course-title-en").get_text(strip=True)
    #     title_zh = item.select_one(".course-title-zh").get_text(strip=True)
    #     description = item.select_one(".course-desc").get_text(strip=True)
    #     url = BASE + item.select_one("a")["href"]
    #     credits_text = item.select_one(".credits").get_text(strip=True)
    #     course = {
    #         "id": f"ABS-{counter:03d}",
    #         "title_en": title_en,
    #         "title_zh": title_zh,
    #         "school": "Alliance Bible Seminary",
    #         "school_zh": "建道神學院",
    #         "school_url": BASE,
    #         "level": detect_level(title_en + " " + description),
    #         "themes": [],        # TODO: extract from tags/categories
    #         "bible_books": [],   # TODO: extract from keywords
    #         "description": description,
    #         "credits": extract_credits(credits_text),
    #         "url": url,
    #         "semester": "",      # TODO: extract from page
    #     }
    #     courses.append(course)
    #     counter += 1
    #     polite_sleep()

    log.warning("ABS scraper is a stub — returning empty list")
    return courses


def scrape_cgst() -> list[dict[str, Any]]:
    """
    China Graduate School of Theology (中國神學研究院)
    https://www.cgst.edu
    """
    # BASE = "https://www.cgst.edu"
    log.warning("CGST scraper is a stub — returning empty list")
    return []


def scrape_lts() -> list[dict[str, Any]]:
    """
    Lutheran Theological Seminary (信義宗神學院)
    https://www.lts.edu.hk
    """
    # BASE = "https://www.lts.edu.hk"
    log.warning("LTS scraper is a stub — returning empty list")
    return []


def scrape_evan() -> list[dict[str, Any]]:
    """
    Evangel Seminary (播道神學院)
    https://www.es.edu.hk
    """
    # BASE = "https://www.es.edu.hk"
    log.warning("Evangel scraper is a stub — returning empty list")
    return []


def scrape_hkbts() -> list[dict[str, Any]]:
    """
    Hong Kong Baptist Theological Seminary (浸信會神學院)
    https://www.hkbts.edu.hk
    """
    # BASE = "https://www.hkbts.edu.hk"
    log.warning("HKBTS scraper is a stub — returning empty list")
    return []


def scrape_ccds() -> list[dict[str, Any]]:
    """
    Chung Chi Divinity School, CUHK (崇基學院神學組)
    https://www.cuhk.edu.hk/theology
    """
    # BASE = "https://www.cuhk.edu.hk/theology"
    log.warning("CCDS scraper is a stub — returning empty list")
    return []


def scrape_gtc() -> list[dict[str, Any]]:
    """
    Grace Theological College (恩福神學院)
    https://www.gtchk.org
    """
    # BASE = "https://www.gtchk.org"
    log.warning("GTC scraper is a stub — returning empty list")
    return []


def scrape_ats() -> list[dict[str, Any]]:
    """
    Alliance Theological Seminary (宣道神學院)
    https://www.ats.edu.hk
    """
    # BASE = "https://www.ats.edu.hk"
    log.warning("ATS scraper is a stub — returning empty list")
    return []


# ── Registry ──────────────────────────────────────────────────────────────────

SCRAPERS: dict[str, tuple[str, str, Any]] = {
    "abs":   ("Alliance Bible Seminary",              "建道神學院",      scrape_abs),
    "cgst":  ("China Graduate School of Theology",    "中國神學研究院",  scrape_cgst),
    "lts":   ("Lutheran Theological Seminary",         "信義宗神學院",    scrape_lts),
    "evan":  ("Evangel Seminary",                      "播道神學院",      scrape_evan),
    "hkbts": ("Hong Kong Baptist Theological Seminary","浸信會神學院",    scrape_hkbts),
    "ccds":  ("Chung Chi Divinity School (CUHK)",      "崇基學院神學組",  scrape_ccds),
    "gtc":   ("Grace Theological College",             "恩福神學院",      scrape_gtc),
    "ats":   ("Alliance Theological Seminary",         "宣道神學院",      scrape_ats),
}


# ── Main ──────────────────────────────────────────────────────────────────────

def run(school_keys: list[str], dry_run: bool, merge: bool) -> None:
    collected: list[dict[str, Any]] = []

    for key in school_keys:
        if key not in SCRAPERS:
            log.error("Unknown school key '%s'. Available: %s", key, list(SCRAPERS))
            continue
        name_en, name_zh, fn = SCRAPERS[key]
        log.info("Scraping %s (%s) …", name_en, name_zh)
        try:
            results = fn()
            log.info("  → %d courses collected", len(results))
            collected.extend(results)
        except Exception as exc:
            log.error("  ✗ %s: %s", name_en, exc)

    if not collected:
        log.warning("No courses collected from any scraper.")

    if merge and DATA_FILE.exists():
        with DATA_FILE.open(encoding="utf-8") as fh:
            existing: list[dict[str, Any]] = json.load(fh)
        existing_ids = {c["id"] for c in existing}
        new_courses = [c for c in collected if c["id"] not in existing_ids]
        log.info("Merging %d new courses into %d existing courses", len(new_courses), len(existing))
        collected = existing + new_courses

    if dry_run:
        print(json.dumps(collected, ensure_ascii=False, indent=2))
    else:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("w", encoding="utf-8") as fh:
            json.dump(collected, fh, ensure_ascii=False, indent=2)
        log.info("Written %d courses to %s", len(collected), DATA_FILE)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scrape theology courses from Hong Kong seminary websites."
    )
    parser.add_argument(
        "--school",
        metavar="KEY",
        help=(
            "Scrape only this school. Choices: "
            + ", ".join(SCRAPERS)
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print JSON to stdout instead of writing data/courses.json",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="Replace data/courses.json entirely instead of merging",
    )
    args = parser.parse_args()

    keys = [args.school] if args.school else list(SCRAPERS.keys())
    run(keys, dry_run=args.dry_run, merge=not args.no_merge)


if __name__ == "__main__":
    main()
