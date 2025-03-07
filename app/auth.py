from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlmodel import Session
from app.models.user_models import User
from app.database import get_session
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

SECRET = "YOUR_SECRET_KEY"  # Replace with a secure value

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    user_db_model = User
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.id} has registered.")

async def get_user_manager(session: Session = Depends(get_session)):
    yield UserManager(SQLAlchemyUserDatabase(User, session, User.__table__))

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)