def calculate_score(resume_tokens, job_tokens):
    resume_set = set(resume_tokens)
    job_set = set(job_tokens)

    matched_keywords = resume_set.intersection(job_set)
    missing_keywords = job_set.difference(resume_set)

    score = (len(matched_keywords) / len(job_set)) * 100 if job_set else 0
    return round(score, 2), matched_keywords, missing_keywords


def classify_fit(score):
    if score >= 80:
        return "Excellent Fit"
    elif score >= 60:
        return "Good Fit"
    elif score >= 40:
        return "Average Fit"
    else:
        return "Poor Fit"
