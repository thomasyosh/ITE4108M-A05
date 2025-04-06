import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

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

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI setup
app = FastAPI()

# CRUD endpoints
@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = DBRecipe(
        title=recipe.title,
        date=recipe.date,
        description=recipe.description,
        cooking_time=recipe.cooking_time,
        serving_size=recipe.serving_size
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    # Add ingredients
    for ingredient in recipe.ingredients:
        db_ingredient = DBIngredient(
            recipe_id=db_recipe.id,
            name=ingredient.name,
            quantity=ingredient.quantity
        )
        db.add(db_ingredient)
    
    # Add steps
    for step in recipe.steps:
        db_step = DBStep(
            recipe_id=db_recipe.id,
            step_number=step.step_number,
            instruction=step.instruction
        )
        db.add(db_step)
    
    db.commit()
    return db_recipe

@app.get("/recipes/", response_model=List[Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(DBRecipe).offset(skip).limit(limit).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update recipe fields
    db_recipe.title = recipe.title
    db_recipe.date = recipe.date
    db_recipe.description = recipe.description
    db_recipe.cooking_time = recipe.cooking_time
    db_recipe.serving_size = recipe.serving_size
    
    # Delete existing ingredients and steps
    db.query(DBIngredient).filter(DBIngredient.recipe_id == recipe_id).delete()
    db.query(DBStep).filter(DBStep.recipe_id == recipe_id).delete()
    
    # Add new ingredients
    for ingredient in recipe.ingredients:
        db_ingredient = DBIngredient(
            recipe_id=recipe_id,
            name=ingredient.name,
            quantity=ingredient.quantity
        )
        db.add(db_ingredient)
    
    # Add new steps
    for step in recipe.Steps:
        db_step = DBStep(
            recipe_id=recipe_id,
            step_number=step.step_number,
            instruction=step.instruction
        )
        db.add(db_step)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

@app.get("/step/{step_id}", response_model=Step)
def read_step(step_id: int, db: Session = Depends(get_db)):
    """
    Get a specific step by its ID
    """
    db_step = db.query(DBStep).filter(DBStep.id == step_id).first()
    if db_step is None:
        raise HTTPException(status_code=404, detail="Step not found")
    return db_step
# Run the application
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
