from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.db_context import base


class members(base):
    __tablename__ = "members"

    memebr_id = Column(type_=Integer, primary_key=True,autoincrement=True)
    FirstName = Column(type_=String(150), nullable=False)
    LastName = Column(type_=String(150), nullable=False)
    PhoneNumber = Column(type_=String(20), nullable=True)
    UserName = Column(type_=String(150), nullable=False)
    Password = Column(type_=String(150), nullable=False)
    membership_id = Column(Integer, ForeignKey('membership.Memebership_id'))

    membership = relationship("MemeberShip", back_populates="members")
    membersintask = relationship("MembersInTasks", back_populates="member")