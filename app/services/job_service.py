import pandas as pd
import time

from app.models.job import Job
from app.db.session import SessionLocal
from app.core.celery_app import celery_app

@celery_app.task()
def process_job(job_id: int):
    
    db = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return

        job.status = "running"
        db.commit()

        file_path = f"uploads/{job.file_name}"

        df = pd.read_csv(file_path)

        total = len(df)
        success = 0
        failed = 0
        job.total_rows = total
        db.commit()

        for index, row in df.iterrows():
            try:
                print(f"[JOB {job_id}]  Processing row {index}")
                time.sleep(0.5)
                success +=1
            except Exception as e:
                failed +=1
                
        job.success_count = success
        job.failed_count = failed
        job.status = "completed"
        db.commit()

    except Exception as e:
        if job:
            job.status = "failed"
            db.commit()
        print("Error:", str(e))

    finally:
        db.close()
