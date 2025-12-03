from sqlalchemy.orm import Session
from lib.models.user import User
from lib.models.tool_type import ToolType
from lib.models.tool import Tool
from lib.models.checkout import Checkout
from datetime import datetime

# -- Users
def create_user(db: Session, username: str, full_name: str = "", role: str = "technician"):
    u = User(username=username, full_name=full_name, role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def get_users(db: Session):
    return db.query(User).order_by(User.id).all()

# -- Tool Types
def create_tool_type(db: Session, name: str, description: str = ""):
    tt = ToolType(name=name, description=description)
    db.add(tt)
    db.commit()
    db.refresh(tt)
    return tt

def get_tool_types(db: Session):
    return db.query(ToolType).order_by(ToolType.id).all()

# -- Tools
def create_tool(db: Session, name: str, serial_number: str, type_id: int, location: str = ""):
    t = Tool(name=name, serial_number=serial_number, type_id=type_id, location=location)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

def get_tools(db: Session):
    return db.query(Tool).order_by(Tool.id).all()

def get_tool_by_id(db: Session, tool_id: int):
    return db.query(Tool).filter(Tool.id == tool_id).first()

def get_tool_by_serial(db: Session, serial: str):
    return db.query(Tool).filter(Tool.serial_number == serial).first()

# -- Checkouts
def checkout_tool(db: Session, user_id: int, tool_id: int):
    tool = get_tool_by_id(db, tool_id)
    if not tool:
        return None, "Tool not found"
    if tool.status != "available":
        return None, f"Tool not available (status={tool.status})"
    tool.status = "checked_out"
    co = Checkout(user_id=user_id, tool_id=tool_id)
    db.add(co)
    db.commit()
    db.refresh(co)
    return co, None

def return_tool(db: Session, tool_id: int, condition: str = None):
    tool = get_tool_by_id(db, tool_id)
    if not tool:
        return None, "Tool not found"
    co = db.query(Checkout).filter(Checkout.tool_id == tool_id, Checkout.returned_at.is_(None)).order_by(Checkout.checked_out_at.desc()).first()
    if not co:
        return None, "Tool is not currently checked out"
    co.returned_at = datetime.utcnow()
    co.condition_on_return = condition
    tool.status = "available"
    db.commit()
    db.refresh(co)
    return co, None

def calibrate_tool(db: Session, tool_id: int):
    tool = get_tool_by_id(db, tool_id)
    if not tool:
        return None, "Tool not found"
    tool.last_calibrated = datetime.utcnow()
    tool.status = "available"
    db.commit()
    db.refresh(tool)
    return tool, None

def get_active_checkouts(db: Session):
    return db.query(Checkout).filter(Checkout.returned_at.is_(None)).order_by(Checkout.checked_out_at.desc()).all()
