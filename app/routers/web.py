from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PhoneTI

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")

HARDCODED_USERNAME = "admin"
HARDCODED_PASSWORD = "admin"


def _prefix(request: Request) -> str:
    return request.scope.get("root_path", "")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url=f"{_prefix(request)}/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == HARDCODED_USERNAME and password == HARDCODED_PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url=f"{_prefix(request)}/dashboard", status_code=303)
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid credentials"}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("authenticated"):
        return RedirectResponse(url=f"{_prefix(request)}/", status_code=302)
    records = db.query(PhoneTI).order_by(PhoneTI.id.desc()).all()
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "records": records}
    )


@router.post("/dashboard")
def insert_record(
    request: Request,
    phone_number: str = Form(...),
    ti_number: int = Form(...),
    email: str = Form(""),
    db: Session = Depends(get_db),
):
    if not request.session.get("authenticated"):
        return RedirectResponse(url=f"{_prefix(request)}/", status_code=302)
    new_record = PhoneTI(
        phone_number=phone_number,
        ti_number=ti_number,
        email=email or None,
    )
    db.add(new_record)
    db.commit()
    return RedirectResponse(url=f"{_prefix(request)}/dashboard", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f"{_prefix(request)}/", status_code=302)
