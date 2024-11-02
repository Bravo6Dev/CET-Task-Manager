from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db_context import base


class MemeberShip(base):
    __tablename__ = "membership"

    Memebership_id = Column(type_=Integer, primary_key=True,autoincrement=True)
    Name = Column(type_=String(150), nullable=False)
    members = relationship("members", back_populates="membership")