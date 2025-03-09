from typing import Optional
import uuid
from sqlmodel import SQLModel, Field, Column, String, Boolean
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from fastapi_users import schemas
from pydantic import EmailStr, BaseModel


class User(SQLModelBaseUserDB, table=True):
    __tablename__ = "user"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(sa_column=Column(String, unique=True, nullable=False, index=True))
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False))
    is_superuser: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    is_verified: bool = Field(default=False, sa_column=Column(Boolean, nullable=False))
    first_name: str = Field(default=None, sa_column=Column(String, nullable=True))
    last_name: str = Field(default=None, sa_column=Column(String, nullable=True))

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str = None
    last_name: str = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserDB(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool
    first_name: str = None
    last_name: str = None