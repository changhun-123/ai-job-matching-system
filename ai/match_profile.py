"""Profile-to-job matching logic for the AI Job Matching System.

This MVP module uses simple, explainable rules instead of a complex model.
The goal is to make the score easy to understand and easy to improve later.
"""

from typing import Dict, List, Set


def match_profile_to_job(analyzed_job: Dict[str, object], profile: Dict[str, object]) -> Dict[str, object]:
    """Compare one analyzed job with the user's profile.

    Args:
        analyzed_job: Dictionary created by ai/analyze_jobs.py.
        profile: Dictionary containing skills, experiences, and interests.

    Returns:
        A dictionary with fit_score, fit_reason, missing_skills,
        and highlight_experience.
    """
    profile_skills = normalize_to_set(profile.get("skills", []))
    profile_interests = normalize_to_set(profile.get("interests", []))
    profile_experiences = normalize_to_list(profile.get("experiences", []))

    required_skills = normalize_to_set(analyzed_job.get("required_skills", []))
    job_type = str(analyzed_job.get("job_type", ""))
    keywords = normalize_to_set(analyzed_job.get("keywords", []))
    job_text = " ".join(
        [
            str(analyzed_job.get("summary", "")),
            str(analyzed_job.get("core_tasks", "")),
            str(analyzed_job.get("keywords", "")),
        ]
    ).lower()

    fit_score = 0
    fit_reason = []

    matched_skills = sorted(profile_skills.intersection(required_skills))
    missing_skills = sorted(required_skills.difference(profile_skills))

    # Skill matching is the most important part of the MVP score.
    if required_skills:
        skill_score = int((len(matched_skills) / len(required_skills)) * 60)
        fit_score += skill_score

        if matched_skills:
            fit_reason.append(f"Matched skills: {', '.join(matched_skills)}")
        else:
            fit_reason.append("No required skills matched yet.")
    else:
        fit_score += 20
        fit_reason.append("No required skills were listed, so a basic score was added.")

    # Add points when the job type fits the user's interests.
    interest_score = calculate_interest_score(job_type, keywords, profile_interests)
    fit_score += interest_score

    if interest_score > 0:
        fit_reason.append(f"Job type and keywords align with profile interests: {job_type}")

    # Highlight experiences that look useful for this job.
    highlight_experience = find_highlight_experience(profile_experiences, job_text, keywords)

    if highlight_experience:
        fit_score += min(len(highlight_experience) * 5, 20)
        fit_reason.append("Relevant project experience was found.")

    # Keep the final score between 0 and 100.
    fit_score = min(fit_score, 100)

    return {
        "fit_score": fit_score,
        "fit_reason": fit_reason,
        "missing_skills": missing_skills,
        "highlight_experience": highlight_experience,
    }


def normalize_to_set(value: object) -> Set[str]:
    """Convert a list or comma-separated string into a clean lowercase set."""
    return set(normalize_to_list(value))


def normalize_to_list(value: object) -> List[str]:
    """Convert common input formats into a clean lowercase list."""
    if value is None:
        return []

    if isinstance(value, str):
        items = value.split(",")
    elif isinstance(value, list):
        items = value
    else:
        items = [str(value)]

    return [str(item).strip().lower() for item in items if str(item).strip()]


def calculate_interest_score(job_type: str, keywords: Set[str], profile_interests: Set[str]) -> int:
    """Give extra points when job direction matches the user's interests."""
    score = 0

    if job_type == "AI 활용형" and "ai" in profile_interests:
        score += 15

    if job_type == "서비스/기획형" and any(
        interest in profile_interests for interest in ["cx", "data-driven services"]
    ):
        score += 15

    if job_type == "데이터 분석형" and any(
        interest in profile_interests for interest in ["data-driven services", "ai"]
    ):
        score += 10

    if "customer experience" in keywords and "cx" in profile_interests:
        score += 5

    if "ai" in keywords and "ai" in profile_interests:
        score += 5

    return min(score, 20)


def find_highlight_experience(
    profile_experiences: List[str], job_text: str, keywords: Set[str]
) -> List[str]:
    """Find profile experiences that are relevant to the analyzed job."""
    highlights = []

    for experience in profile_experiences:
        experience_lower = experience.lower()

        if "review" in experience_lower and (
            "text analysis" in keywords or "review" in job_text or "customer" in job_text
        ):
            highlights.append(experience)

        elif "lstm" in experience_lower and (
            "lstm" in keywords or "time series" in keywords or "forecasting" in job_text
        ):
            highlights.append(experience)

        elif "data collection" in experience_lower and (
            "data" in job_text or "pipeline" in job_text or "collection" in job_text
        ):
            highlights.append(experience)

    return highlights
