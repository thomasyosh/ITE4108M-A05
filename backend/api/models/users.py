from typing import Annotated
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Table, Column, Integer, String, Boolean
from pydantic import EmailStr, Field
from ..database import engine
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    email= Column(String(255), unique=True, nullable=False)
    first_name= Column(String(255), unique=True, nullable=False)
    last_name= Column(String(255), unique=True, nullable=False)
    hashed_password= Column(String(255), unique=True, nullable=False)
    provider= Column(String(255), unique=True, nullable=False)
    picture= Column(String(255), unique=True, nullable=False)
    is_active= Column(Boolean, unique=True, nullable=False)
    is_superuser= Column(Boolean, unique=True, nullable=False)

Base.metadata.create_all(engine)