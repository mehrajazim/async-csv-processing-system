from fastapi import APIRouter, UploadFile, Depends, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.db.deps import get_db
from app.models.job import Job
from app.services.job_service import process_job

router = APIRouter()

UPLOAD_DIR = "uploads"


# ---------------------------
# Upload CSV + create job
# ---------------------------
@router.post("/upload-csv/")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create job in DB
    job = Job(
        file_name=file.filename,
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "message": "File uploaded successfully",
        "job_id": job.id,
        "job_status": job.status
    }


# ---------------------------
# Run job (Celery async)
# ---------------------------
@router.post("/run-job/{job_id}")
def run_job(job_id: int):

    # Send task to Celery worker
    process_job.delay(job_id)

    return {
        "message": "Job sent to worker",
        "job_id": job_id
    }


# ---------------------------
# Get job status
# ---------------------------
@router.get("/job/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "file_name": job.file_name,
        "total_rows": job.total_rows,
        "success": job.success_count,
        "failed" : job.failed_count
    }