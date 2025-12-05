from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.db import Base

class Checkout(Base):
    __tablename__ = "checkouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"))
    
    
    
    due_date = Column(DateTime, nullable=False) 
   
    project_location = Column(String, nullable=False) 
    
    
    checked_out_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)
    condition_on_return = Column(String, nullable=True)

    user = relationship("User")
    tool = relationship("Tool", back_populates="checkouts")