from typing import Optional, List
import uuid
from sqlmodel import SQLModel, Field, Relationship

from app.models.user_models import User




class Project(SQLModel, table=True):
    __tablename__ = "project"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    
    tasks: List["Task"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"primaryjoin": "Project.id == Task.project_id"}
    )

class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    
    project: Optional[Project] = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"primaryjoin": "Task.project_id == Project.id"}
    )

Project.model_rebuild(force=True)
Task.model_rebuild(force=True)
