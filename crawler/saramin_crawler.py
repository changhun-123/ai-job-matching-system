"""Saramin crawler for collecting list + detail job text.

This crawler first collects jobs from a Saramin search page,
then visits each detail page to extract the full posting text.
"""

from __future__ import annotations

from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup



BASE_URL = "https://www.saramin.co.kr"
SEARCH_URL = f"{BASE_URL}/zf_user/search"
REQUEST_TIMEOUT = 12

def fetch_soup(url: str, headers: dict[str, str]) -> BeautifulSoup:
    """Download one page and return BeautifulSoup."""
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def fetch_html(url: str, headers: dict[str, str]) -> str:
    """Download raw HTML for pages that should be stored as-is."""
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def extract_deadline(item: BeautifulSoup) -> str:
    """Extract deadline text from a search result card."""
    deadline_node = item.select_one(".job_date .date")

    if deadline_node and deadline_node.text.strip():
        return deadline_node.text.strip()

    return "확인필요"


def extract_body_text(page_soup: BeautifulSoup) -> str:
    """Extract all text inside body without keyword/noise pre-filtering."""
    body = page_soup.select_one("body")
    if not body:
        return ""
    return body.get_text("\n", strip=True)


def extract_iframe_job_html(
    detail_soup: BeautifulSoup, headers: dict[str, str], page_url: str
) -> str:
    """Extract full HTML from Saramin relay iframe if present."""
    iframe = (
        detail_soup.select_one("iframe#iframe_content_0")
        or detail_soup.select_one("iframe#iframe_content")
        or detail_soup.select_one("iframe.iframe_content")
        or detail_soup.select_one("iframe[src*='/zf_user/jobs/relay/']")
    )

    if not iframe:
        return ""

    iframe_src = iframe.get("src", "").strip()

    if not iframe_src:
        return ""

    iframe_url = urljoin(page_url, iframe_src)

    try:
        return fetch_html(iframe_url, headers=headers)
    except requests.RequestException:
        return ""


def extract_iframe_body_text(iframe_html: str) -> str:
    """Extract all text from iframe page body."""
    if not iframe_html:
        return ""

    iframe_soup = BeautifulSoup(iframe_html, "html.parser")
    return extract_body_text(iframe_soup)


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
        iframe_html = ""

        try:
            detail_soup = fetch_soup(url, headers=headers)
            iframe_html = extract_iframe_job_html(
                detail_soup, headers=headers, page_url=url
            )

            if iframe_html:
                iframe_body_text = extract_iframe_body_text(iframe_html)
                if iframe_body_text:
                    job_text = iframe_body_text
                else:
                    detail_body_text = extract_body_text(detail_soup)
                    if detail_body_text:
                        job_text = detail_body_text
            else:
                detail_body_text = extract_body_text(detail_soup)
                if detail_body_text:
                    job_text = detail_body_text
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
                "job_html": iframe_html,
            }
        )

    return jobs
