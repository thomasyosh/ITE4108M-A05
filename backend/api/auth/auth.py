from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID
import secrets

from fastapi import Depends, HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
import jwt
from ..models.users import User
from ..schemas import *
from passlib.context import CryptContext
from ..database import session
from sqlalchemy import exc

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY: str = secrets.token_urlsafe(32)

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)

async def authenticate_user(email: str, password: str):
    user = await session.query(User).filter_by(email=email).one()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt