from fastapi import FastAPI
from app.db.session import Base, engine
from app.models.job import Job
from app.api.routes import router



app = FastAPI(title = 'CSV to API Automation System')

Base.metadata.create_all(bind = engine)

app.include_router(router)


@app.get("/")
def health_chekc():
    return {"status":"ok", "message": "running"}
