from fastapi import Depends, Request, Cookie, APIRouter
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    JWTStrategy,
    CookieTransport,
    BearerTransport,
    AuthenticationBackend,
)
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from sqlmodel import Session
from app.models.user_models import User
from app.database import get_session
from passlib.context import CryptContext
import uuid
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create a CryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    '''
    Get the password hash
    '''
    return pwd_context.hash(password)

# Get the secret key from the environment
SECRET = os.getenv("SECRET")


# Create a separate function to get user_db
def get_user_db(session: Session = Depends(get_session)):
    yield SQLModelUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLModelUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_name="projectauth",
    cookie_max_age=3600,  # 1 hour
    cookie_secure=False,  # Set to True in production with HTTPS
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)



auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(optional=True, active=True)

