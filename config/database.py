"""SQLite helper functions for the AI Job Matching System."""

import sqlite3
from pathlib import Path
from typing import Any

from config.settings import DATABASE_PATH


def get_connection(db_path=DATABASE_PATH):
    """Create and return a SQLite database connection."""
    return sqlite3.connect(db_path)


def initialize_database(db_path=DATABASE_PATH):
    """Create the database folder and tables if they do not exist yet."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    schema_path = Path(__file__).with_name("schema.sql")

    with get_connection(db_path) as conn:
        with open(schema_path, "r", encoding="utf-8") as schema_file:
            conn.executescript(schema_file.read())


def insert_raw_jobs(jobs, db_path=DATABASE_PATH):
    """Insert raw job postings into the raw_jobs table.

    Duplicate job URLs are ignored, which makes crawling safe to run
    multiple times while developing.
    """
    with get_connection(db_path) as conn:
        conn.executemany(
            """
            INSERT OR IGNORE INTO raw_jobs (
                site,
                title,
                company,
                deadline,
                url,
                job_text
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    job["site"],
                    job["title"],
                    job["company"],
                    job["deadline"],
                    job["url"],
                    job["job_text"],
                )
                for job in jobs
            ],
        )


def fetch_all_raw_jobs(db_path=DATABASE_PATH) -> list[dict[str, Any]]:
    """Fetch all raw jobs ordered by newest first."""
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM raw_jobs ORDER BY id DESC").fetchall()

    return [dict(row) for row in rows]


def count_rows(table_name, db_path=DATABASE_PATH):
    """Return the number of rows in a table.

    The table name is checked against an allow-list because SQLite parameters
    cannot be used for table names.
    """
    allowed_tables = {"raw_jobs", "analyzed_jobs", "matched_jobs"}

    if table_name not in allowed_tables:
        raise ValueError(f"Unknown table name: {table_name}")

    with get_connection(db_path) as conn:
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
