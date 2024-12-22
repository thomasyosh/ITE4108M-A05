from pydantic import BaseModel, Field
import datetime

class Item(BaseModel):
    name: str = Field(default='John Doe')
    
    
class FormData(BaseModel):
    pk_id: int
    name: str
    is_active: bool
    model_config = {"extra": "forbid"}