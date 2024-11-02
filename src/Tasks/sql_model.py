from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.db.db_context import base


class Task(base):
    __tablename__ = "tasks"
    task_id = Column(type_=Integer, primary_key=True,autoincrement=True)
    task_name = Column(type_=String(150), nullable=False)
    description = Column(type_=String(150), nullable=True)
    deadline = Column(type_=String(150), nullable=False)
    status = Column(type_=Integer, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    project = relationship("Project", back_populates="tasks")
    membersintask = relationship("MembersInTasks", back_populates="task")