from typing import Any
from datetime import timedelta
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import RedirectResponse
from ..models import *
from ..schemas import * 
from ..auth.auth import *


router = APIRouter()