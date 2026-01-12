"""Unit tests for domain logic in scorer and text_preprocessing.

These tests validate the behavior of calculate_score, classify_fit,
and preprocess_text independently of the web layer.
"""

import re

from src.scorer import calculate_score, classify_fit
from src.text_preprocessing import preprocess_text


def test_calculate_score_all_keywords_match():
    resume_tokens = ["python", "nlp", "ml"]
    job_tokens = ["python", "nlp"]

    score, matched, missing = calculate_score(resume_tokens, job_tokens)

    assert score == 100.0
    assert matched == {"python", "nlp"}
    assert missing == set()


def test_calculate_score_partial_match():
    resume_tokens = ["python", "sql"]
    job_tokens = ["python", "nlp", "ml"]

    score, matched, missing = calculate_score(resume_tokens, job_tokens)

    # 1 of 3 job keywords matched -> 33.33...
    assert round(score, 2) == 33.33
    assert matched == {"python"}
    assert missing == {"nlp", "ml"}


def test_calculate_score_empty_job_tokens():
    resume_tokens = ["python", "sql"]
    job_tokens = []

    score, matched, missing = calculate_score(resume_tokens, job_tokens)

    assert score == 0
    assert matched == set()
    assert missing == set()


def test_classify_fit_thresholds():
    assert classify_fit(85) == "Excellent Fit"
    assert classify_fit(80) == "Excellent Fit"
    assert classify_fit(79.99) == "Good Fit"
    assert classify_fit(60) == "Good Fit"
    assert classify_fit(59.99) == "Average Fit"
    assert classify_fit(40) == "Average Fit"
    assert classify_fit(39.99) == "Poor Fit"


def test_preprocess_text_basic_tokenization_and_cleanup():
    text = "Python, SQL & data-engineering!!!"

    tokens = preprocess_text(text)

    # Ensure lowercase and punctuation removal have been applied.
    joined = " ".join(tokens)
    assert "python" in tokens
    assert "sql" in tokens
    # No punctuation or symbols should remain
    assert not re.search(r"[^a-z\s]", joined)
