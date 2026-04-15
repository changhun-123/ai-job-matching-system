"""Project-wide settings."""

from pathlib import Path


# Root folder of the project.
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database file. It will be created automatically when main.py runs.
DATABASE_PATH = BASE_DIR / "data" / "jobs.db"

