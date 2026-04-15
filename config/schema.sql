-- SQLite schema for the AI Job Matching System MVP.
-- The tables are intentionally simple so the project stays beginner-friendly.

CREATE TABLE IF NOT EXISTS raw_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT,
    title TEXT,
    company TEXT,
    deadline TEXT,
    url TEXT UNIQUE,
    job_text TEXT
);

CREATE TABLE IF NOT EXISTS analyzed_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_job_id INTEGER NOT NULL,
    summary TEXT,
    required_skills TEXT,
    preferred_skills TEXT,
    job_type TEXT,
    analyzed_at TEXT NOT NULL,
    FOREIGN KEY (raw_job_id) REFERENCES raw_jobs (id)
);

CREATE TABLE IF NOT EXISTS matched_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_job_id INTEGER NOT NULL,
    analyzed_job_id INTEGER,
    fit_score REAL NOT NULL,
    matched_skills TEXT,
    missing_skills TEXT,
    match_reason TEXT,
    matched_at TEXT NOT NULL,
    FOREIGN KEY (raw_job_id) REFERENCES raw_jobs (id),
    FOREIGN KEY (analyzed_job_id) REFERENCES analyzed_jobs (id)
);

