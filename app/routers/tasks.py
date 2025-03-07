from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from fastapi.templating import Jinja2Templates
from app.auth import current_active_user
from app.database import get_session
from app.models.project_models import Task, Project

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_tasks(request: Request, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    # If no tasks are found, return an empty list.
    if not tasks:
        tasks = []
    return templates.TemplateResponse("tasks/list.html", {"request": request, "tasks": tasks})


@router.get("/create", response_class=HTMLResponse)
def create_task_form(request: Request, session: Session = Depends(get_session)):
    # Retrieve projects so the user can associate the new task with a project.
    projects = session.exec(select(Project)).all()
    return templates.TemplateResponse("tasks/create.html", {"request": request, "projects": projects})


@router.post("/create")
def create_task(
    title: str = Form(...),
    project_id: int = Form(...),
    session: Session = Depends(get_session)
):
    task = Task(title=title, project_id=project_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return RedirectResponse(url="/tasks/", status_code=303)
