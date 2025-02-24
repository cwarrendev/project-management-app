from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from fastapi.templating import Jinja2Templates

from app.database import get_session  # Updated import
from app.models import Task, Project  # Updated import if needed

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_tasks(request: Request, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
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
