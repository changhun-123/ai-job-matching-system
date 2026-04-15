import pandas as pd
from crawler.saramin_crawler import collect_saramin_jobs

jobs = collect_saramin_jobs()

print("수집된 공고 수:", len(jobs))

df = pd.DataFrame(jobs)

df.to_csv("jobs_preview.csv", index=False, encoding="utf-8-sig")

print("CSV 저장 완료")