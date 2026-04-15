"""SQLite database setup for the AI Job Matching System.

This module keeps the database code simple and beginner-friendly.
It creates a local SQLite file named jobs.db and provides helper functions
for saving and reading raw job postings.
"""

import sqlite3
from datetime import datetime
from pathlib import Path


# Project root folder: one level above this db/ folder.
BASE_DIR = Path(__file__).resolve().parent.parent

# The SQLite database file created by this project.
DB_PATH = BASE_DIR / "jobs.db"


def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create all database tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Stores job postings exactly as collected by the crawler.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS raw_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            title TEXT,
            site TEXT,
            deadline TEXT,
            url TEXT UNIQUE,
            job_text TEXT,
            created_at TEXT
        )
        """
    )

    # Stores AI analysis results for each raw job posting.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyzed_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            summary TEXT,
            core_tasks TEXT,
            required_skills TEXT,
            preferred_skills TEXT,
            job_type TEXT,
            keywords TEXT
        )
        """
    )

    # Stores matching results between a job posting and the user's profile.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS matched_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            fit_score INTEGER,
            fit_reason TEXT,
            missing_skills TEXT,
            highlight_experience TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def insert_raw_job(job):
    """Insert one raw job posting into the raw_jobs table.

    The job parameter should be a dictionary with these keys:
    company, title, site, deadline, url, and job_text.
    """
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().isoformat(timespec="seconds")

    # INSERT OR IGNORE prevents duplicate jobs when the same URL already exists.
    cursor.execute(
        """
        INSERT OR IGNORE INTO raw_jobs (
            company,
            title,
            site,
            deadline,
            url,
            job_text,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job.get("company"),
            job.get("title"),
            job.get("site"),
            job.get("deadline"),
            job.get("url"),
            job.get("job_text"),
            created_at,
        ),
    )

    conn.commit()
    conn.close()


def fetch_all_raw_jobs():
    """Fetch all raw job postings from the database.

    Returns:
        A list of dictionaries, where each dictionary represents one job.
    """
    conn = get_connection()

    # This setting allows rows to behave like dictionaries.
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM raw_jobs ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
