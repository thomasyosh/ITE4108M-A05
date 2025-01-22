from typing import Any
from uuid import UUID
from pydantic.networks import EmailStr
from sqlalchemy import exc
from fastapi import APIRouter, Body, Depends, HTTPException

from ..database import session
from ..models.users import User
from ..schemas import users
from ..auth.auth import (
    # get_current_active_superuser,
    # get_current_active_user,
    get_hashed_password,
)

router = APIRouter()

@router.post("", response_model=users.User)
async def register_user(
    password: str = Body(...),
    email: EmailStr = Body(...),
    first_name: str = Body(None),
    last_name: str = Body(None),
):
    hashed_password = get_hashed_password(password)
    user = User(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
    )
    try:
        session.add(user)
        session.commit()
    except exc.SQLAlchemyError as e:
        return e