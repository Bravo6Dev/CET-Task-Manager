from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from db.db_context import base

class Project(base):
    __tablename__ = 'projects'
    
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_Name = Column(String(100), nullable=False)
    deadline = Column(DateTime, nullable=False)
    tasks = relationship("Task", back_populates="project")