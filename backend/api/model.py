from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from post_item import Base
from pydantic import BaseModel
from datetime import date
from typing import List

import os
from datetime import date

db_type = os.getenv("DATABASE_TYPE")
db_connection = None

if db_type == "postgres":
    engine = create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}")
    db_connection = engine



# Database setup
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@database-1.cmxnkws8hcin.us-east-1.rds.amazonaws.com/food'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBRecipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(500))
    cooking_time = Column(String(100))
    serving_size = Column(String(100))
    
    ingredients = relationship("DBIngredient", back_populates="recipe", cascade="all, delete-orphan")
    steps = relationship("DBStep", back_populates="recipe", cascade="all, delete-orphan")

class DBIngredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    name = Column(String(100), nullable=False)
    quantity = Column(String(50))
    
    recipe = relationship("DBRecipe", back_populates="ingredients")

class DBStep(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    step_number = Column(Integer, nullable=False)
    instruction = Column(String(500), nullable=False)
    
    recipe = relationship("DBRecipe", back_populates="steps")

# Pydantic models (you already had these)
class Recipe(BaseModel):
    id: int
    title: str
    date: date
    description: str
    cooking_time: str
    serving_size: str
    ingredients: List["Ingredient"] = []
    steps: List["Step"] = []

    class Config:
        orm_mode = True

class Ingredient(BaseModel):
    id: int
    recipe_id: int
    name: str
    quantity: str

    class Config:
        orm_mode = True

class Step(BaseModel):
    id: int
    recipe_id: int
    step_number: int
    instruction: str

    class Config:
        orm_mode = True
