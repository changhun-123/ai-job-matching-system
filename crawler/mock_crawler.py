"""Mock crawler for the AI Job Matching System MVP.

This file acts like a real crawler, but it uses fixed sample data instead of
visiting job websites. Later, you can replace the sample data with code that
requests web pages, parses job postings, and returns the same dictionary format.
"""


def collect_mock_jobs():
    """Return sample job postings as a list of dictionaries.

    A future real crawler should return the same keys:
    company, title, site, deadline, url, and job_text.
    """
    return [
        {
            "company": "Insight Lab",
            "title": "Junior Data Analyst",
            "site": "MockJobs",
            "deadline": "2026-05-10",
            "url": "https://example.com/jobs/junior-data-analyst",
            "job_text": (
                "Analyze customer behavior data, create dashboards, and write "
                "reports using Python, SQL, and basic statistics. Experience "
                "with text analysis or service planning is preferred."
            ),
        },
        {
            "company": "Future CX",
            "title": "AI Service Planner",
            "site": "MockJobs",
            "deadline": "2026-05-15",
            "url": "https://example.com/jobs/ai-service-planner",
            "job_text": (
                "Plan AI-powered customer experience services. Work with data "
                "analysts and engineers to define user problems, service flows, "
                "and metrics. Interest in AI, CX, and data-driven services is "
                "important."
            ),
        },
        {
            "company": "ForecastWorks",
            "title": "Time Series Forecasting Intern",
            "site": "MockJobs",
            "deadline": "2026-05-20",
            "url": "https://example.com/jobs/time-series-intern",
            "job_text": (
                "Support forecasting projects using Python and time series "
                "analysis. Knowledge of LSTM models, data preprocessing, and "
                "model evaluation is a plus."
            ),
        },
        {
            "company": "DataBridge",
            "title": "Text Data Analyst",
            "site": "MockJobs",
            "deadline": "2026-05-25",
            "url": "https://example.com/jobs/text-data-analyst",
            "job_text": (
                "Collect and analyze review, survey, and customer feedback text "
                "data. Build keyword summaries, classify VOC topics, and present "
                "insights for product and service improvement."
            ),
        },
        {
            "company": "ServiceAI Studio",
            "title": "Data-Driven Service Planning Assistant",
            "site": "MockJobs",
            "deadline": "2026-05-31",
            "url": "https://example.com/jobs/service-planning-assistant",
            "job_text": (
                "Support service planning projects using market research, user "
                "data, and AI trend analysis. Prepare planning documents, define "
                "customer journey problems, and suggest data-based service ideas."
            ),
        },
    ]
