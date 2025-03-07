import asyncio
from sqlmodel import Session, select
from app.database import engine
from app.models.user_models import User, UserCreate
from app.auth import get_user_manager

async def create_test_user():

    # Open a synchronous session.
    with Session(engine) as session:
        # get_user_manager is now corrected to yield the right UserManager instance.
        manager = None
        async for mgr in get_user_manager(session):
            manager = mgr
            break  # Only need the first instance.

        if manager is None:
            print("User manager not initialized.")
            return

        # Check if the test user already exists.
        existing_user = session.exec(
            select(User).where(User.email == "test@example.com")
        ).first()
        if existing_user:
            print("Test user already exists:", existing_user.email)
            return

        # Create a UserCreate model with the test user's data.
        user_data = UserCreate(email="test@example.com", password="test")
        # Create the user (this call is async).
        test_user = await manager.create(user_data)
        print("Test user created:", test_user.email)

if __name__ == "__main__":
    asyncio.run(create_test_user())