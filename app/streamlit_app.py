"""Streamlit dashboard for the AI Job Matching System.

Run this file with:
    streamlit run app/streamlit_app.py

The dashboard first tries to load raw jobs from SQLite. If the database is
empty, it uses the mock crawler data so the app still works as a demo.
"""

from collections import Counter
from pathlib import Path
import sys

import pandas as pd
import streamlit as st


# Add the project root to Python's import path.
# This lets Streamlit import modules from ai/, crawler/, and config/.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from ai.analyze_jobs import analyze_job
from ai.match_profile import match_profile_to_job
from crawler.mock_crawler import collect_mock_jobs
from config.database import fetch_all_raw_jobs, initialize_database, insert_raw_jobs


# User profile used for the MVP matching logic.
PROFILE = {
    "skills": [
        "Python",
        "data analysis",
        "text analysis",
        "time series analysis",
        "service planning",
    ],
    "experiences": [
        "co-living review analysis project",
        "LSTM forecasting project",
        "data collection environment setup",
    ],
    "interests": ["AI", "CX", "data-driven services"],
}


def load_jobs() -> pd.DataFrame:
    """Load job data from SQLite and create analysis/matching columns.

    If SQLite has no raw jobs yet, mock jobs are inserted first.
    """
    initialize_database()

    raw_jobs = fetch_all_raw_jobs()

    # Use sample data when the database is empty.
    if not raw_jobs:
        insert_raw_jobs(collect_mock_jobs())
        raw_jobs = fetch_all_raw_jobs()

    dashboard_rows = []

    for job in raw_jobs:
        analyzed_job = analyze_job(job["job_text"])
        matched_job = match_profile_to_job(analyzed_job, PROFILE)

        dashboard_rows.append(
            {
                "company": job["company"],
                "title": job["title"],
                "site": job["site"],
                "deadline": job["deadline"],
                "url": job["url"],
                "summary": analyzed_job["summary"],
                "core_tasks": analyzed_job["core_tasks"],
                "required_skills": analyzed_job["required_skills"],
                "preferred_skills": analyzed_job["preferred_skills"],
                "job_type": analyzed_job["job_type"],
                "keywords": analyzed_job["keywords"],
                "fit_score": matched_job["fit_score"],
                "fit_reason": ", ".join(matched_job["fit_reason"]),
                "missing_skills": ", ".join(matched_job["missing_skills"]),
                "highlight_experience": ", ".join(matched_job["highlight_experience"]),
            }
        )

    return pd.DataFrame(dashboard_rows)


def split_comma_text(value: str) -> list[str]:
    """Split a comma-separated text value into a clean list."""
    if not value:
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


def show_job_list(df: pd.DataFrame) -> None:
    """Display the main job list table."""
    st.subheader("Job List")
    st.dataframe(
        df[
            [
                "company",
                "title",
                "site",
                "deadline",
                "job_type",
                "required_skills",
                "fit_score",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


def show_fit_score_ranking(df: pd.DataFrame) -> None:
    """Display jobs sorted by fit score."""
    st.subheader("Fit Score Ranking")

    ranking_df = df.sort_values(by="fit_score", ascending=False)

    st.bar_chart(
        ranking_df,
        x="title",
        y="fit_score",
        color="#2E86AB",
    )

    st.dataframe(
        ranking_df[["company", "title", "fit_score", "fit_reason"]],
        use_container_width=True,
        hide_index=True,
    )


def show_job_type_distribution(df: pd.DataFrame) -> None:
    """Display how many jobs belong to each job type."""
    st.subheader("Job Type Distribution")

    job_type_df = df["job_type"].value_counts().reset_index()
    job_type_df.columns = ["job_type", "count"]

    st.bar_chart(job_type_df, x="job_type", y="count", color="#4CAF50")


def show_required_skills_summary(df: pd.DataFrame) -> None:
    """Display the most common required skills."""
    st.subheader("Required Skills Summary")

    skill_counter = Counter()

    for skills_text in df["required_skills"]:
        skill_counter.update(split_comma_text(skills_text))

    skill_df = pd.DataFrame(skill_counter.items(), columns=["skill", "count"])
    skill_df = skill_df.sort_values(by="count", ascending=False)

    if skill_df.empty:
        st.info("No required skills found yet.")
    else:
        st.bar_chart(skill_df, x="skill", y="count", color="#F18F01")
        st.dataframe(skill_df, use_container_width=True, hide_index=True)


def show_job_details(df: pd.DataFrame) -> None:
    """Let the user inspect one job in more detail."""
    st.subheader("Job Details")

    selected_title = st.selectbox("Select a job", df["title"].tolist())
    selected_job = df[df["title"] == selected_title].iloc[0]

    st.write(f"**Company:** {selected_job['company']}")
    st.write(f"**Deadline:** {selected_job['deadline']}")
    st.write(f"**Job Type:** {selected_job['job_type']}")
    st.write(f"**Fit Score:** {selected_job['fit_score']}")
    st.write(f"**Summary:** {selected_job['summary']}")
    st.write(f"**Core Tasks:** {selected_job['core_tasks']}")
    st.write(f"**Missing Skills:** {selected_job['missing_skills']}")
    st.write(f"**Highlight Experience:** {selected_job['highlight_experience']}")
    st.link_button("Open Job Posting", selected_job["url"])


def main() -> None:
    """Render the Streamlit dashboard."""
    st.set_page_config(page_title="AI Job Matching System", layout="wide")

    st.title("AI Job Matching System")
    st.write("Simple MVP dashboard for analyzed job postings and profile matching.")

    jobs_df = load_jobs()

    if jobs_df.empty:
        st.warning("No job data found.")
        return

    # Top-level summary metrics.
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", len(jobs_df))
    col2.metric("Average Fit Score", round(jobs_df["fit_score"].mean(), 1))
    col3.metric("Best Fit Score", int(jobs_df["fit_score"].max()))

    show_job_list(jobs_df)

    left_col, right_col = st.columns(2)

    with left_col:
        show_fit_score_ranking(jobs_df)

    with right_col:
        show_job_type_distribution(jobs_df)
        show_required_skills_summary(jobs_df)

    show_job_details(jobs_df)


if __name__ == "__main__":
    main()
