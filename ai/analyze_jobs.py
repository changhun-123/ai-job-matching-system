"""Rule-based job posting analysis for the AI Job Matching System.

This MVP module does not use an external AI model yet. It uses simple keyword
rules so the project can work immediately and be improved later.
"""

from typing import Dict, List


# Skills we want to detect in job postings.
SKILL_KEYWORDS = {
    "Python": ["python", "파이썬"],
    "SQL": ["sql"],
    "statistics": ["statistics", "statistical", "통계"],
    "AI": ["ai", "artificial intelligence", "인공지능"],
    "machine learning": ["machine learning", "ml", "머신러닝"],
    "service planning": ["service planning", "서비스 기획", "기획"],
}


# Keywords used to classify the general job type.
JOB_TYPE_KEYWORDS = {
    "데이터 분석형": [
        "data analysis",
        "analyst",
        "analytics",
        "dashboard",
        "statistics",
        "데이터 분석",
        "분석",
    ],
    "서비스/기획형": [
        "service planning",
        "service planner",
        "planning",
        "customer journey",
        "서비스 기획",
        "기획",
    ],
    "AI 활용형": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "lstm",
        "model",
        "인공지능",
        "머신러닝",
    ],
    "엔지니어링형": [
        "engineering",
        "engineer",
        "backend",
        "api",
        "pipeline",
        "database",
        "엔지니어",
        "개발",
    ],
}


def analyze_job(job_text: str) -> Dict[str, str]:
    """Analyze one job posting and return structured information.

    Args:
        job_text: Full text of a job posting.

    Returns:
        A dictionary with summary, core_tasks, required_skills,
        preferred_skills, job_type, and keywords.
    """
    clean_text = job_text.strip()
    lower_text = clean_text.lower()

    detected_skills = detect_skills(lower_text)
    job_type = classify_job_type(lower_text)
    keywords = extract_keywords(lower_text)

    return {
        "summary": make_summary(clean_text),
        "core_tasks": extract_core_tasks(clean_text, lower_text),
        "required_skills": ", ".join(detected_skills),
        "preferred_skills": infer_preferred_skills(lower_text, detected_skills),
        "job_type": job_type,
        "keywords": ", ".join(keywords),
    }


def detect_skills(lower_text: str) -> List[str]:
    """Find important skills mentioned in the job posting."""
    detected_skills = []

    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword in lower_text for keyword in keywords):
            detected_skills.append(skill)

    return detected_skills


def classify_job_type(lower_text: str) -> str:
    """Classify a job posting into one of four simple job types."""
    scores = {}

    for job_type, keywords in JOB_TYPE_KEYWORDS.items():
        scores[job_type] = sum(1 for keyword in keywords if keyword in lower_text)

    best_job_type = max(scores, key=scores.get)

    # If no classification keywords are found, use a general default.
    if scores[best_job_type] == 0:
        return "데이터 분석형"

    return best_job_type


def make_summary(job_text: str) -> str:
    """Create a short summary from the first sentence or first part of the text."""
    if not job_text:
        return "채용 공고 내용이 비어 있습니다."

    first_sentence = job_text.split(".")[0].strip()

    if len(first_sentence) > 120:
        first_sentence = first_sentence[:117] + "..."

    return first_sentence


def extract_core_tasks(job_text: str, lower_text: str) -> str:
    """Create a simple task summary based on keywords in the posting."""
    tasks = []

    if any(word in lower_text for word in ["analyze", "analysis", "analytics", "분석"]):
        tasks.append("데이터 분석")

    if any(word in lower_text for word in ["dashboard", "report", "보고서"]):
        tasks.append("리포트 및 대시보드 작성")

    if any(word in lower_text for word in ["planning", "service", "customer journey", "기획"]):
        tasks.append("서비스 기획")

    if any(word in lower_text for word in ["model", "machine learning", "lstm", "forecasting"]):
        tasks.append("AI/머신러닝 모델 활용")

    if not tasks:
        return make_summary(job_text)

    return ", ".join(tasks)


def infer_preferred_skills(lower_text: str, detected_skills: List[str]) -> str:
    """Infer preferred skills using simple clue words."""
    preferred_skills = []

    if any(word in lower_text for word in ["preferred", "plus", "nice to have", "우대"]):
        preferred_skills.extend(detected_skills)

    if "cx" in lower_text or "customer experience" in lower_text:
        preferred_skills.append("CX understanding")

    if "text analysis" in lower_text or "review" in lower_text or "voc" in lower_text:
        preferred_skills.append("text analysis")

    return ", ".join(dict.fromkeys(preferred_skills))


def extract_keywords(lower_text: str) -> List[str]:
    """Extract a small list of useful keywords from the job text."""
    possible_keywords = [
        "python",
        "sql",
        "statistics",
        "ai",
        "machine learning",
        "service planning",
        "data analysis",
        "dashboard",
        "customer experience",
        "text analysis",
        "time series",
        "lstm",
    ]

    return [keyword for keyword in possible_keywords if keyword in lower_text]
