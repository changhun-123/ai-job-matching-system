import requests
from bs4 import BeautifulSoup


def collect_saramin_jobs(keyword="데이터 분석"):
    url = f"https://www.saramin.co.kr/zf_user/search?searchword={keyword}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    items = soup.select(".item_recruit")

    for item in items:
        try:
            title = item.select_one(".job_tit a").text.strip()
            company = item.select_one(".corp_name a").text.strip()
            link = "https://www.saramin.co.kr" + item.select_one(".job_tit a")["href"]

            jobs.append({
                "company": company,
                "title": title,
                "site": "Saramin",
                "deadline": "확인필요",
                "url": link,
                "job_text": title
            })

        except:
            continue

    return jobs