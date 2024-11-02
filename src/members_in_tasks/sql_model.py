from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.db_context import base

class MembersInTasks(base):
    __tablename__ = "membersintask"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=False, )
    task = relationship("Task", back_populates="membersintask")
    member_id = Column(Integer, ForeignKey('members.memebr_id'),  nullable=False)
    member = relationship("members", back_populates="membersintask")