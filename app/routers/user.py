from fastapi import APIRouter, Depends, HTTPException
from app.models.user_models import User, UserCreate
from app.auth import get_user_manager, UserManager
from fastapi_users_db_sqlmodel import SQLModelUserDatabase

router = APIRouter()

@router.post("/create-user", response_model=User)
async def create_user(user_data: UserCreate, user_manager: UserManager = Depends(get_user_manager)):
    # Check if the user already exists.
    user_data = UserCreate(email="test@example.com", password="test")
    existing_user = await user_manager.user_db.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # Create the user.
    created_user = await user_manager.create(user_data)
    return created_user