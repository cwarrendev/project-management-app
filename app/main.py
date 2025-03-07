from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.database import engine, create_db_and_tables
from app.routers import projects, tasks, dashboard
from app.routers.user import router as user_router
from app.auth import fastapi_users, auth_backend, current_active_user
from app.database import get_session
from app.models.user_models import UserCreate, UserDB, User
from typing import Optional
import logging
logging.basicConfig(level=logging.DEBUG)



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")




@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user = Depends(current_active_user)):
    if user is not None:
        # If already logged in, go to home page
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, user: User | None = Depends(current_active_user)):
    logging.info(f"User: {user}")
    if user is None:
        # If not logged in, redirect to login page
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request})



# Include your existing routers
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(user_router, prefix="/users", tags=["Users"])

# Include FastAPI-Users routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserDB, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
