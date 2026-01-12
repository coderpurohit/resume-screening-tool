from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from .use_cases.resume_screening import screen_resume


class ScreenRequest(BaseModel):
    """Request body for JSON-based resume screening."""

    resume_text: str
    job_description: str


class ScreenResponse(BaseModel):
    """Standard response payload for resume screening results."""

    score: float
    fit: str
    matched_keywords: List[str]
    missing_keywords: List[str]


app = FastAPI(title="Resume Screening API")


@app.get("/")
async def health_check() -> dict:
    """Simple health check endpoint."""

    return {"status": "ok", "service": "resume-screening-api"}


@app.post("/analyze", response_model=ScreenResponse)
async def analyze_resume(payload: ScreenRequest) -> ScreenResponse:
    """Analyze resume and job description provided as raw text.

    This endpoint is useful when the client already has the resume text extracted.
    """

    score, fit, matched, missing = screen_resume(
        resume_text=payload.resume_text,
        job_text=payload.job_description,
    )

    # Ensure deterministic ordering in the response
    return ScreenResponse(
        score=score,
        fit=fit,
        matched_keywords=sorted(matched),
        missing_keywords=sorted(missing),
    )


@app.post("/upload", response_model=ScreenResponse)
async def upload_resume(
    file: UploadFile = File(..., description="Resume file (plain text recommended)"),
    job_description: str = Form(..., description="Job description text"),
) -> ScreenResponse:
    """Upload a resume file and analyze it against the given job description.

    For now, the implementation assumes a text-based resume (e.g., .txt).
    If a binary format (like PDF/DOCX) is uploaded, the file is decoded as UTF-8
    and non-decodable characters are ignored. In a production system, this is
    where you'd plug in a proper document parser.
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="No resume file provided.")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded resume file is empty.")

    try:
        resume_text = raw_bytes.decode("utf-8", errors="ignore")
    except Exception as exc:  # pragma: no cover - very defensive
        raise HTTPException(status_code=400, detail="Could not decode resume file.") from exc

    score, fit, matched, missing = screen_resume(
        resume_text=resume_text,
        job_text=job_description,
    )

    return ScreenResponse(
        score=score,
        fit=fit,
        matched_keywords=sorted(matched),
        missing_keywords=sorted(missing),
    )
