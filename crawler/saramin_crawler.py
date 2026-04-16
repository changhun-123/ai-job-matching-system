"""Saramin crawler for collecting list + detail job text.

This crawler first collects jobs from a Saramin search page,
then visits each detail page to extract the full posting text.
"""

from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.saramin.co.kr"
SEARCH_URL = f"{BASE_URL}/zf_user/search"
REQUEST_TIMEOUT = 12


def normalize_text(text: str) -> str:
    """Collapse excessive whitespace for cleaner storage."""
    return " ".join(text.split())


def fetch_soup(url: str, headers: dict[str, str]) -> BeautifulSoup:
    """Download one page and return BeautifulSoup."""
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_deadline(item: BeautifulSoup) -> str:
    """Extract deadline text from a search result card."""
    deadline_node = item.select_one(".job_date .date")

    if deadline_node and deadline_node.text.strip():
        return deadline_node.text.strip()

    return "확인필요"


def extract_job_text(detail_soup: BeautifulSoup, fallback_title: str) -> str:
    """Extract detail page description text with safe fallbacks."""
    detail_candidates = [
        ".wrap_jv_cont",
        ".job_article",
        "#content",
        ".contWrap",
    ]

    for selector in detail_candidates:
        section = detail_soup.select_one(selector)

        if section:
            extracted = normalize_text(section.get_text(" ", strip=True))

            if len(extracted) >= 50:
                return extracted

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
