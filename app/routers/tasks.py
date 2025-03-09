from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlmodel import Session, select
from fastapi.templating import Jinja2Templates
from app.auth import current_active_user
from app.database import get_session
from app.models.project_models import Task, Project
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def list_tasks(request: Request, session: Session = Depends(get_session), user=Depends(current_active_user)):
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    tasks = session.exec(select(Task)).all()
    # If no tasks are found, return an empty list.
    if not tasks:
        tasks = []
    return templates.TemplateResponse("tasks/list.html", {"request": request, "tasks": tasks})


@router.get("/create", response_class=HTMLResponse)
def create_task_form(request: Request, session: Session = Depends(get_session), user=Depends(current_active_user)):
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    # Retrieve projects so the user can associate the new task with a project.
    projects = session.exec(select(Project)).all()
    return templates.TemplateResponse("tasks/create.html", {"request": request, "projects": projects})


@router.post("/create")
def create_task(
    title: str = Form(...),
    project_id: int = Form(...),
    session: Session = Depends(get_session),
    user=Depends(current_active_user)
):
    '''
    Create a new task.
    '''
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    task = Task(title=title, project_id=project_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return RedirectResponse(url="/tasks/", status_code=303)

class TaskUpdate(BaseModel):
    completed: Optional[bool] = None


@router.post("/{task_id}/toggle-completion")
def toggle_task_completion(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    user=Depends(current_active_user)
):
    '''
    Handles toggling the completion status of a task.
    '''
    if user is None:
        return JSONResponse(status_code=401, content={"message": "Not authenticated"})
    
    # Find the task
    task = session.get(Task, task_id)
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    
    # Update the task completion status
    task.completed = task_update.completed
    session.add(task)
    session.commit()
    
    return JSONResponse(content={"success": True, "completed": task.completed})