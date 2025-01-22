from typing import Any
from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import RedirectResponse
from ..models import *
from ..schemas.tokens import Token
from ..auth.auth import *


router = APIRouter()

@router.post("/access-token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }