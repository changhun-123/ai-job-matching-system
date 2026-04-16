"""Main entry point for the AI Job Matching System MVP.

Workflow:
1. Create the SQLite database and tables.
2. Run mock crawler data insertion.
3. Run Saramin crawler and store detail job text.
4. Print raw_jobs row count summary.
"""

from crawler.mock_crawler import collect_mock_jobs
from crawler.saramin_crawler import collect_saramin_jobs
from config.database import count_rows, initialize_database, insert_raw_jobs
from config.settings import DATABASE_PATH


def main() -> None:
    """Run the MVP workflow with both mock and Saramin crawlers."""
    print("Starting AI Job Matching System MVP...")

    initialize_database()
    print(f"Database is ready: {DATABASE_PATH}")

    mock_jobs = collect_mock_jobs()
    insert_raw_jobs(mock_jobs)
    print(f"Mock crawler collected {len(mock_jobs)} jobs.")

    try:
        saramin_jobs = collect_saramin_jobs(keyword="데이터 분석", limit=20)
        insert_raw_jobs(saramin_jobs)
        print(f"Saramin crawler collected {len(saramin_jobs)} jobs.")
    except Exception as error:
        print(f"Saramin crawler skipped due to error: {error}")

    raw_job_count = count_rows("raw_jobs")
    print(f"raw_jobs table now contains {raw_job_count} jobs.")


if __name__ == "__main__":
    main()
