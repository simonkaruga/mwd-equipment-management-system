from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from lib.db import get_db, Base, engine
from lib import crud, models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MWD Tool Management")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# ---------------- Home ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- Users ----------------
@app.get("/users", response_class=HTMLResponse)
def users(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/users/add")
def add_user(
    username: str = Form(...),
    full_name: str = Form(...),
    role: str = Form("technician"),
    db: Session = Depends(get_db)
):
    crud.create_user(db, username, full_name, role)
    return RedirectResponse("/users", status_code=303)


# ---------------- Tool Types ----------------
@app.get("/tool-types", response_class=HTMLResponse)
def tool_types(request: Request, db: Session = Depends(get_db)):
    types = crud.get_tool_types(db)
    return templates.TemplateResponse("tool_types.html", {"request": request, "types": types})

@app.post("/tool-types/add")
def add_tool_type(name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    crud.create_tool_type(db, name, description)
    return RedirectResponse("/tool-types", status_code=303)


# ---------------- Tools ----------------
@app.get("/tools", response_class=HTMLResponse)
def tools(request: Request, db: Session = Depends(get_db)):
    tools = crud.get_tools(db)
    return templates.TemplateResponse("tools.html", {"request": request, "tools": tools, "types": crud.get_tool_types(db)})

@app.post("/tools/add")
def add_tool(
    name: str = Form(...),
    serial_number: str = Form(...),
    type_id: int = Form(...),
    location: str = Form(""),
    db: Session = Depends(get_db)
):
    crud.create_tool(db, name, serial_number, type_id, location)
    return RedirectResponse("/tools", status_code=303)


# ---------------- Checkouts ----------------
@app.get("/checkouts", response_class=HTMLResponse)
def checkouts(request: Request, db: Session = Depends(get_db)):
    active = crud.get_active_checkouts(db)
    return templates.TemplateResponse("checkouts.html", {"request": request, "checkouts": active})

@app.post("/checkouts/checkout")
def checkout_tool(user_id: int = Form(...), tool_id: int = Form(...), db: Session = Depends(get_db)):
    co, err = crud.checkout_tool(db, user_id, tool_id)
    return RedirectResponse("/checkouts", status_code=303)

@app.post("/checkouts/return")
def return_tool(tool_id: int = Form(...), condition: str = Form("Good"), db: Session = Depends(get_db)):
    co, err = crud.return_tool(db, tool_id, condition)
    return RedirectResponse("/checkouts", status_code=303)
