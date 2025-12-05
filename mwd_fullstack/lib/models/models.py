from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class ToolType(Base):
    __tablename__ = "tool_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    tools = relationship("Tool", back_populates="tool_type")


class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    tool_id = Column(String, unique=True)
    type_id = Column(Integer, ForeignKey("tool_types.id"))
    status = Column(String, default="Available")

    tool_type = relationship("ToolType", back_populates="tools")
