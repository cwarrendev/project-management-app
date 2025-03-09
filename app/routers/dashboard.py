from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth import current_active_user
from app.database import get_session
from app.models.project_models import Project, Task
from sqlmodel import Session, select
from sqlalchemy import func



router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, session: Session = Depends(get_session), user=Depends(current_active_user)):
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    projects = session.exec(select(Project)).all()
    total_projects = len(projects)
    
    tasks = session.exec(select(Task)).all()
    total_tasks = len(tasks)
    
    completed = session.exec(select(Task).where(Task.completed == True)).all()
    completed_tasks = len(completed)
    
    tasks_by_project = {}
    for project in projects:
        count = session.exec(
            select(func.count(Task.id)).where(Task.project_id == project.id)
        ).one()  # Returns an int
        tasks_by_project[project.name] = count

    metrics = {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "tasks_by_project": tasks_by_project
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "metrics": metrics})