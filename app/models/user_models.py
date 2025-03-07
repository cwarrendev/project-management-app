from typing import Optional
import uuid
from sqlmodel import SQLModel, Field, Column, String, Boolean
from fastapi_users.db import SQLAlchemyBaseUserTable
from pydantic import EmailStr, BaseModel

# Place SQLModel first to ensure __table__ is built properly.
class User(SQLModel, SQLAlchemyBaseUserTable, table=True):
    __tablename__ = "user"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(sa_column=Column(String, unique=True, nullable=False, index=True))
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    is_superuser: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    is_verified: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    
    class Config:
        arbitrary_types_allowed = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserDB(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool