from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.db import Base

class ToolType(Base):
    __tablename__ = "tool_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    tools = relationship("Tool", back_populates="tool_type")
