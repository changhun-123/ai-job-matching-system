"""Main entry point for the AI Job Matching System MVP.

Current MVP step:
1. Create the SQLite database and tables.
2. Run a mock crawler.
3. Save collected job postings into the raw_jobs table.

Later steps will add AI analysis, profile matching, and the Streamlit app.
"""

from crawler.mock_crawler import collect_mock_jobs
from config.database import count_rows, initialize_database, insert_raw_jobs
from config.settings import DATABASE_PATH


def main():
    """Run the first MVP workflow."""
    print("Starting AI Job Matching System MVP...")

    initialize_database()
    print(f"Database is ready: {DATABASE_PATH}")

    jobs = collect_mock_jobs()
    insert_raw_jobs(jobs)

    raw_job_count = count_rows("raw_jobs")
    print(f"Mock crawler collected {len(jobs)} jobs.")
    print(f"raw_jobs table now contains {raw_job_count} jobs.")


if __name__ == "__main__":
    main()
