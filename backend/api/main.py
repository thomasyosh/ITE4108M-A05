from fastapi import FastAPI, Form, HTTPException, status, Depends
import os
from peewee import *
import psycopg2
import pymysql
from .model import Testing, BaseModel, db_connection
from .post_item import Item, FormData
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import json
from .routers.api import api_router
from .models.users import User

app = FastAPI(
    title=os.getenv("PROJECT_NAME"),
    root_path= "/api",
    docs_url="/docs"
    )

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def connection():
    try:
        with db_connection.connection_context() as db:
            return db_connection.close()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Database error, please check env file")
     
def fake_hash_password(password: str):
    return "fakehashed" + password

@app.get("/connection")
async def test():
    return connection()

@app.get("/")
async def read_all():
    if connection():
        query = Testing.select().order_by(Testing.pk_id).dicts()
        return list(query)

@app.get("/testing")
async def read_item(pk_id: int):
    if connection():
        query = Testing().select().where(Testing.pk_id == pk_id)
        if query.exists():
            return query.dicts().get()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.post("/testing")
async def root(item: Item):
    if connection():
        data = Testing()
        data.name = item.name
        data.save()
        query = Testing().select().where(Testing.pk_id == data.pk_id).dicts().get()
        return query

@app.put("/update")
async def update_record(data: Annotated[FormData, Form()]) -> None:
    if connection():
        query = Testing()\
            .select()\
                .where(
                    Testing.pk_id == data.pk_id
                    )
        if query.exists():
            update_data = Testing().update({Testing.name:data.name, Testing.is_active:data.is_active}).where(Testing.pk_id == data.pk_id)
            update_data.execute()
        else:
            raise HTTPException(status_code=404, detail="Item not found")
        query = Testing().select().where(Testing.pk_id == data.pk_id).dicts().get()
        return query

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

if __name__ == "__main__":
    print(1)