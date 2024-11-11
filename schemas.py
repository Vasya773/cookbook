from pydantic import BaseModel
from typing import Optional


class BaseRecipes(BaseModel):
    name: str
    number_views: int = 0
    cooking_time: int

class RecipesIn(BaseRecipes):
    ...

class RecipesOut(BaseRecipes):
    recipe_id: int

    class Config:
        from_attributes = True

class BaseDeepRecipes(BaseModel):
    name: str
    ingredients: str
    description: Optional[str] = None

class DeepRecipesIn(BaseDeepRecipes):
    ...

class DeepRecipesOut(BaseDeepRecipes):
    recipe_id: int

    class Config:
        from_attributes = True
