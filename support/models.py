from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from database import Base


class FAQ(Base):
    __tablename__ = "FAQ"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    text = Column(String)

    parent_id = Column(Integer, ForeignKey('FAQ.id'), nullable=True)
    children = relationship("FAQ", cascade="all,delete", backref=backref('parent', remote_side=[id]))

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)