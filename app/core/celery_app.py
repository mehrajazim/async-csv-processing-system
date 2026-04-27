from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
import app.services.job_service

# 🔥 IMPORTANT: force import tasks
# celery_app.conf.imports = ("app.services.job_service",)
# celery_app.autodiscover_tasks(["app"])