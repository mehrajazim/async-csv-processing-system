from sqlalchemy import Integer, DateTime, Column, String
from datetime import datetime
from app.db.session import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, index = True, primary_key = True)
    file_name = Column(String, nullable = False)
    status = Column(String, default = "pending")
    created_at = Column(DateTime, default = datetime.utcnow)
    
    total_rows = Column(Integer,default=0)
    success_count = Column(Integer,default=0)
    failed_count = Column(Integer,default=0)
