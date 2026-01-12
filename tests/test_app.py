"""Tests for the FastAPI application endpoints.

These tests exercise only the web layer and treat the underlying
resume_screening use-case as a black box.
"""

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "resume-screening-api"


def test_analyze_resume_returns_expected_shape():
    payload = {
        "resume_text": "Experienced engineer with Python and data analysis skills.",
        "job_description": "Looking for an engineer with strong Python skills.",
    }

    response = client.post("/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    # Basic shape checks
    assert set(data.keys()) == {"score", "fit", "matched_keywords", "missing_keywords"}
    assert isinstance(data["score"], (int, float))
    assert isinstance(data["fit"], str)
    assert isinstance(data["matched_keywords"], list)
    assert isinstance(data["missing_keywords"], list)


def test_analyze_resume_validation_error_when_missing_fields():
    # Missing job_description field
    payload = {"resume_text": "Only resume text provided"}

    response = client.post("/analyze", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (validation error)


def test_upload_resume_with_text_file(tmp_path):
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("Python data engineering", encoding="utf-8")

    with resume_path.open("rb") as f:
        files = {"file": ("resume.txt", f, "text/plain")}
        data = {"job_description": "Python engineering"}

        response = client.post("/upload", files=files, data=data)

    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"score", "fit", "matched_keywords", "missing_keywords"}
