from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from lib.db import get_db, Base, engine
from lib import crud, models

from lib.db import SessionLocal

Base.metadata.create_all(bind=engine)

from lib.db import SessionLocal  

def seed_database():
    db = SessionLocal()
    try:
        
        if db.query(models.ToolType).first() is None:
           
            tool_types_data = [
                ("Drilling Bits", "Fixed cutter and roller cone drill bits for various formations"),
                ("Measurement While Drilling (MWD)", "Real-time downhole measurement tools for directional data"),
                ("Logging While Drilling (LWD)", "Formation evaluation tools that measure petrophysical properties"),
                ("Directional Drilling Tools", "Bent housing motors, rotary steerable systems for wellbore navigation"),
                ("Downhole Motors", "Positive displacement motors for directional drilling"),
                ("Stabilizers", "Blades and sleeve stabilizers for wellbore stability"),
                ("Reamers", "Hole enlargement tools and back reamers"),
                ("Drill Pipe", "Heavy weight drill pipe and drill collars"),
                ("Mud Motors", "Turbodrilling motors and performance motors"),
                ("Survey Instruments", "Multi-shot and single-shot survey tools")
            ]

            for name, description in tool_types_data:
                crud.create_tool_type(db, name, description)

            
            users_data = [
                ("john_kamau", "John Kamau", "john.kamau@gmail.com", "drilling_engineer"),
                ("prince_kibali", "Prince Kibali", "prince.kibali@gmail.com", "mwd_technician"),
                ("simon_njoroge", "Simon Njoroge", "simon.njoroge@gmail.com", "tool_push"),
                ("edwin_omondi", "Edwin Omondi", "edwin.omondi@gmail.com", "mud_engineer"),
                ("ann_kwamboka", "Ann Kwamboka", "ann.kwamboka@gmail.com", "rig_manager")
            ]

            for username, full_name, email, role in users_data:
                crud.create_user(db, username, full_name, email, role)

          
            tools_data = [
                ("PDC Bit 8.5\"", "MWDBIT-001", 1, "Drill Bits Storage"),
                ("Tricone Bit 12.25\"", "MWDBIT-002", 1, "Drill Bits Storage"),
                ("PDC Bit 6\"", "MWDBIT-003", 1, "Drill Bits Storage"),

                ("PowerPulse MWD System", "MWDSYS-001", 2, "MWD Electronics Bay"),
                ("TeleScope MWD Tool", "MWDSYS-002", 2, "MWD Electronics Bay"),
                ("SlimPulse MWD", "MWDSYS-003", 2, "MWD Electronics Bay"),

                ("EcoScope Multiple Propagation Resistivity", "LWDTOOL-001", 3, "LWD Tool Storage"),
                ("SonicVision Sonic Tool", "LWDTOOL-002", 3, "LWD Tool Storage"),
                ("Azimuthal Litho-Density Tool", "LWDTOOL-003", 3, "LWD Tool Storage"),

                ("Navi-Drill RSS", "DDSYS-001", 4, "Directional Tools Bay"),
                ("PowerDrive RSS", "DDSYS-002", 4, "Directional Tools Bay"),
                ("AutoTrak RSS", "DDSYS-003", 4, "Directional Tools Bay"),

                ("Hamilton Motor 8\"", "DHMOTOR-001", 5, "Downhole Motors Storage"),
                ("Navi-Drill X-treme Motor", "DHMOTOR-002", 5, "Downhole Motors Storage"),
                ("PowerPak Motor", "DHMOTOR-003", 5, "Downhole Motors Storage"),

                ("Spiral Blade Stabilizer 8.5\"", "STABIL-001", 6, "Stabilizers Storage"),
                ("Integral Blade Stabilizer", "STABIL-002", 6, "Stabilizers Storage"),
                ("String Stabilizer", "STABIL-003", 6, "Stabilizers Storage"),
            ]

            for name, serial_number, type_id, location in tools_data:
                crud.create_tool(db, name, serial_number, type_id, location)

        db.commit()
        print(" Database seeded with initial MWD equipment data")
    except Exception as e:
        print(f" Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

seed_database()


app = FastAPI(title="MWD Tool Management")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    types = crud.get_tool_types(db)
    return templates.TemplateResponse("index.html", {"request": request, "major_tool_types": types})

@app.get("/users", response_class=HTMLResponse)
def users(request: Request, db: Session = Depends(get_db)):
    users_db = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})

@app.post("/users/add")
def add_user(
    username: str = Form(...),
    full_name: str = Form(""),
    email: str = Form(""),
    role: str = Form("technician"),
    db: Session = Depends(get_db)
):
    crud.create_user(db, username, full_name, email, role)
    return RedirectResponse("/users", status_code=303)

@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return RedirectResponse("/users", status_code=303)
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post("/users/edit/{user_id}")
def update_user(
    user_id: int,
    username: str = Form(...),
    full_name: str = Form(""),
    email: str = Form(""),
    role: str = Form("technician"),
    db: Session = Depends(get_db)
):
    user = crud.update_user(db, user_id, username, full_name, email, role)
    return RedirectResponse("/users", status_code=303)

@app.post("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return RedirectResponse("/users", status_code=303)

@app.get("/tool-types", response_class=HTMLResponse)
def tool_types(request: Request, db: Session = Depends(get_db)):
    tool_types_list = crud.get_tool_types(db)
    return templates.TemplateResponse("tool_types.html", {"request": request, "tool_types": tool_types_list})

@app.post("/tool-types/add")
def add_tool_type(name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    crud.create_tool_type(db, name, description)
    return RedirectResponse("/tool-types", status_code=303)

@app.get("/tool-types/edit/{tool_type_id}", response_class=HTMLResponse)
def edit_tool_type(tool_type_id: int, request: Request, db: Session = Depends(get_db)):
    tt = db.query(models.ToolType).filter(models.ToolType.id == tool_type_id).first()
    if not tt:
        return RedirectResponse("/tool-types", status_code=303)
    return templates.TemplateResponse("edit_tool_type.html", {"request": request, "tool_type": tt})

@app.post("/tool-types/edit/{tool_type_id}")
def update_tool_type(
    tool_type_id: int,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    tt = crud.update_tool_type(db, tool_type_id, name, description)
    return RedirectResponse("/tool-types", status_code=303)

@app.post("/tool-types/delete/{tool_type_id}")
def delete_tool_type(tool_type_id: int, db: Session = Depends(get_db)):
    crud.delete_tool_type(db, tool_type_id)
    return RedirectResponse("/tool-types", status_code=303)

@app.get("/tools", response_class=HTMLResponse)
def tools(request: Request, search: str = "", db: Session = Depends(get_db)):
    all_tools = crud.get_tools(db)

    if search:
        tools_db = [tool for tool in all_tools
                if search.lower() in tool.name.lower() or
                   search.lower() in tool.serial_number.lower()]
    else:
        tools_db = all_tools

    return templates.TemplateResponse("tools.html", {
        "request": request,
        "tools": tools_db,
        "types": crud.get_tool_types(db),
        "search_query": search
    })

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

@app.get("/checkouts", response_class=HTMLResponse)
def checkouts(request: Request, db: Session = Depends(get_db)):
    active = crud.get_active_checkouts(db)
    return templates.TemplateResponse("checkouts.html", {"request": request, "checkouts": active})

@app.get("/checkouts/new", response_class=HTMLResponse)
def new_checkout(request: Request, db: Session = Depends(get_db)):
    users_db = crud.get_users(db)
    available_tools = crud.get_available_tools(db)
    return templates.TemplateResponse("add_checkout.html", {
        "request": request,
        "users": users_db,
        "available_tools": available_tools
    })

@app.post("/checkouts/checkout")
def checkout_tool(
    user_id: int = Form(...),
    tool_id: int = Form(...),
    project_location: str = Form(...),
    due_date: str = Form(...),
    db: Session = Depends(get_db)
):
    co, err = crud.checkout_tool(db, user_id, tool_id, project_location, due_date)
    return RedirectResponse("/checkouts", status_code=303)

@app.post("/checkouts/return")
def return_tool(tool_id: int = Form(...), condition: str = Form("Good"), db: Session = Depends(get_db)):
    co, err = crud.return_tool(db, tool_id, condition)
    return RedirectResponse("/checkouts", status_code=303)
