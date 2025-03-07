from typing import Optional
import uuid
from sqlmodel import SQLModel, Field
from fastapi_users.db import SQLAlchemyBaseUserTable
from pydantic import EmailStr, BaseModel

# Let the base class supply email, hashed_password, etc.
class User(SQLAlchemyBaseUserTable, SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    
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