from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.db import Base

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey("tool_types.id"))
    location = Column(String, nullable=True)
    status = Column(String, default="available")
    last_calibrated = Column(DateTime, default=datetime.utcnow)

    tool_type = relationship("ToolType", back_populates="tools")

    checkouts = relationship("Checkout", back_populates="tool")
