from pydantic import BaseModel, Field
import datetime

class Recipe(BaseModel):
    id: int
    title: str
    date: datetime.date
    description: str
    cooking_time: str
    serving_size: str

class Ingredient(BaseModel):
    id: int
    recipe_id: int
    name: str
    quantity: str

class Step(BaseModel):
    id: int
    recipe_id: int
    step_number: int
    instruction: str