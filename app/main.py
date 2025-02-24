from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.database import engine, create_db_and_tables
from app.routers import projects, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database and tables if they do not exist
    create_db_and_tables()
    yield
    # Place shutdown code here if needed

app = FastAPI(lifespan=lifespan)

# Mount static files (if you add custom CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")




@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


# Include routers
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)