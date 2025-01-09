from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    status = Column(String, default="created")
    result = Column(Integer, nullable=True)
