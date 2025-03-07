from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from fastapi.templating import Jinja2Templates
from app.auth import current_active_user
from app.database import get_session
from app.models.project_models import Project

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_projects(request: Request, session: Session = Depends(get_session), user=Depends(current_active_user)):
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    projects = session.exec(select(Project)).all()
    return templates.TemplateResponse("projects/list.html", {"request": request, "projects": projects})


@router.get("/create", response_class=HTMLResponse)
def create_project_form(request: Request):
    return templates.TemplateResponse("projects/create.html", {"request": request})


@router.post("/create")
def create_project(
    name: str = Form(...),
    description: str = Form(None),
    session: Session = Depends(get_session)
):
    project = Project(name=name, description=description)
    session.add(project)
    session.commit()
    session.refresh(project)
    return RedirectResponse(url="/projects/", status_code=303)
