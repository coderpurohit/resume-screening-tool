"""Use-case for screening a resume against a job description.

This module is framework-agnostic and can be used from CLI, web APIs, or other adapters.
"""

from ..text_preprocessing import preprocess_text
from ..scorer import calculate_score, classify_fit


def screen_resume(resume_text: str, job_text: str):
    """Run the resume screening pipeline.

    Returns a tuple of (score, fit_label, matched_keywords, missing_keywords).
    """

    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_text)

    score, matched, missing = calculate_score(resume_tokens, job_tokens)
    fit = classify_fit(score)
    return score, fit, matched, missing
