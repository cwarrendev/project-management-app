# app/models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

    # Relationship to tasks (one-to-many)
    tasks: List["Task"] = Relationship(back_populates="project")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")

    # Relationship back to project
    project: Optional[Project] = Relationship(back_populates="tasks")
