from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.routers import projects, tasks, dashboard
from app.routers.user import router as user_router
from app.auth import fastapi_users, auth_backend, current_active_user
from app.database import get_session
from app.models.user_models import UserCreate, UserDB
from app.models.project_models import Project, Task


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Create the FastAPI app and disable the default docs and redoc routes
app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add the Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    '''
    This route renders the login page.
    '''
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/logout")
async def custom_logout():
    '''
    Logs the user out and deletes the cookie.
    '''
    response = RedirectResponse(url="/login")
    response.delete_cookie(
        "projectauth",
        domain=None,
        path="/"
    )
    return response

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, user=Depends(current_active_user)):
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    
    # Return template with all data
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
        }
    )


# Routers
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(user_router, prefix="/users", tags=["Users"])


# Include FastAPI-Users routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/cookie",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserDB, UserCreate), prefix="/auth", tags=["auth"]
)
