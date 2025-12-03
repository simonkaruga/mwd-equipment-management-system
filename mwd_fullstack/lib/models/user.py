from sqlalchemy import Column, Integer, String
from lib.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="technician")
