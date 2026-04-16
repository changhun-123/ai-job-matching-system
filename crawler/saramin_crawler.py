"""Saramin crawler for collecting list + detail job text.

This crawler first collects jobs from a Saramin search page,
then visits each detail page to extract the full posting text.
"""

from __future__ import annotations

import json
import re
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup



BASE_URL = "https://www.saramin.co.kr"
SEARCH_URL = f"{BASE_URL}/zf_user/search"
REQUEST_TIMEOUT = 12

JOB_KEYWORD_PATTERN = re.compile(
    r"(모집|자격|우대|업무|근무|학력|경력|기술|스킬|지원|전형|연봉|복지)"
)
NOISE_PHRASES = (
    "로그인",
    "회원가입",
    "메뉴",
    "홈",
    "채용정보",
    "포지션 제안",
    "커뮤니티",
    "닫기",
    "이전공고",
    "다음공고",
)


def normalize_text(text: str) -> str:
    """Collapse excessive whitespace for cleaner storage."""
    return " ".join(text.split())


def fetch_soup(url: str, headers: dict[str, str]) -> BeautifulSoup:
    """Download one page and return BeautifulSoup."""
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")



def looks_like_noise(text: str) -> bool:
    """Heuristic filter to reject nav-heavy or repetitive text blobs."""
    if len(text) < 80:
        return True

    noise_hits = sum(text.count(phrase) for phrase in NOISE_PHRASES)

    if noise_hits >= 6:
        return True

    if not JOB_KEYWORD_PATTERN.search(text):
        return True

    # Reject extremely repetitive sequences.
    first_chunk = text[:120]

    if first_chunk and text.count(first_chunk) >= 3:
        return True

    return False


def clean_section_text(section: BeautifulSoup) -> str:
    """Extract text from a section after removing known noise tags."""
    section_clone = BeautifulSoup(str(section), "html.parser")

    for node in section_clone.select(
        "script, style, noscript, header, footer, nav, .blind, .skip, .ad, .banner"
    ):
        node.decompose()

    text_nodes = section_clone.select("h1, h2, h3, h4, p, li, dt, dd, th, td, span")

    if text_nodes:
        merged = " ".join(node.get_text(" ", strip=True) for node in text_nodes)
    else:
        merged = section_clone.get_text(" ", strip=True)

    return normalize_text(merged)


def extract_from_structured_data(detail_soup: BeautifulSoup) -> str:
    """Try structured JSON-LD first because it often has cleaner descriptions."""
    for script in detail_soup.select("script[type='application/ld+json']"):
        raw_json = script.string or script.get_text(strip=True)

        if not raw_json:
            continue

        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            continue

        candidates: list[str] = []

        if isinstance(data, dict):
            value = data.get("description")
            if isinstance(value, str):
                candidates.append(value)

        if isinstance(data, list):
            for row in data:
                if isinstance(row, dict) and isinstance(row.get("description"), str):
                    candidates.append(row["description"])

        for candidate in candidates:
            normalized = normalize_text(candidate)
            if not looks_like_noise(normalized):
                return normalized

    return ""


def extract_deadline(item: BeautifulSoup) -> str:
    """Extract deadline text from a search result card."""
    deadline_node = item.select_one(".job_date .date")

    if deadline_node and deadline_node.text.strip():
        return deadline_node.text.strip()

    return "확인필요"


def extract_job_text(detail_soup: BeautifulSoup, fallback_title: str) -> str:
    """Extract detail page description text with safe fallbacks."""
    from_json = extract_from_structured_data(detail_soup)

    if from_json:
        return from_json

    detail_candidates = [
        ".wrap_jv_cont .user_content",
        ".wrap_jv_cont .cont",
        ".wrap_jv_cont",
        ".job_article",
        "#content",
        ".contWrap",
    ]

    for selector in detail_candidates:
        section = detail_soup.select_one(selector)

        if not section:
            continue

        extracted = clean_section_text(section)

        if not looks_like_noise(extracted):
            return extracted

    # Final fallback: use page-level text but keep quality gate to avoid menu garbage.
    page_text = normalize_text(detail_soup.get_text(" ", strip=True))

    if not looks_like_noise(page_text):
        return page_text

    return fallback_title


def collect_saramin_jobs(keyword: str = "데이터 분석", limit: int = 20) -> list[dict[str, str]]:
    """Collect Saramin jobs and include detail-page body text.

    Args:
        keyword: Search keyword for Saramin.
        limit: Max number of postings to collect from the first page.

    Returns:
        List of dictionaries with company, title, site, deadline, url, job_text.
    """
    search_url = f"{SEARCH_URL}?searchword={quote_plus(keyword)}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    soup = fetch_soup(search_url, headers=headers)
    jobs = []

    items = soup.select(".item_recruit")

    for item in items[:limit]:
        title_node = item.select_one(".job_tit a")
        company_node = item.select_one(".corp_name a")

        if not title_node or not company_node:
            continue

        title = title_node.text.strip()
        company = company_node.text.strip()
        href = title_node.get("href", "")

        if not href:
            continue

        url = f"{BASE_URL}{href}"
        deadline = extract_deadline(item)

        job_text = title

        try:
            detail_soup = fetch_soup(url, headers=headers)
            job_text = extract_job_text(detail_soup, fallback_title=title)
        except requests.RequestException:
            # Keep fallback title text when a detail page is unavailable.
            pass

        jobs.append(
            {
                "company": company,
                "title": title,
                "site": "Saramin",
                "deadline": deadline,
                "url": url,
                "job_text": job_text,
            }
        )

    return jobs
