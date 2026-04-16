"""Quick crawler test script.

Collect Saramin jobs (with detail text), preview as CSV,
and save into SQLite raw_jobs for inspection.
"""

import pandas as pd

from config.database import initialize_database, insert_raw_jobs
from crawler.saramin_crawler import collect_saramin_jobs


jobs = collect_saramin_jobs()
print("수집된 공고 수:", len(jobs))

if jobs:
    print("첫 공고 본문 길이:", len(jobs[0]["job_text"]))

df = pd.DataFrame(jobs)
df.to_csv("jobs_preview.csv", index=False, encoding="utf-8-sig")
print("CSV 저장 완료")

initialize_database()
insert_raw_jobs(jobs)
print("DB 저장 완료")
