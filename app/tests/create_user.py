import asyncio
import sys
sys.path.append("C:/dev-projects/project-management-app")  # Add project root to path

from sqlmodel import SQLModel, Session
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from app.database import create_db_and_tables, engine  # Use absolute import
from app.models.user_models import User  # Use absolute import
from passlib.context import CryptContext  # Add this to hash passwords properly

# Create password hash function
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(email: str, password: str):
    # Create the tables if they don't exist
    create_db_and_tables()
    
    # Open a synchronous session (the adapter methods are async)
    with Session(engine) as session:
        # Wrap the session in SQLModelUserDatabase
        # Switch order: session first, then model
        user_db = SQLModelUserDatabase(session, User)
        
        # Prepare user data with properly hashed password
        user_data = {
            "email": email,
            "hashed_password": get_password_hash(password),
            "is_active": True,
            "is_verified": False,
            "is_superuser": False
        }
        
        # Create the user (this method is asynchronous)
        created_user = await user_db.create(user_data)
        print(f"User created successfully with ID: {created_user.id}")

if __name__ == "__main__":
    # Example email and password
    email = "cwarren.dev@gmail.com"
    password = "test"
    
    # Run the async user creation function
    asyncio.run(create_user(email, password))