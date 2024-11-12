from sqlalchemy import Column, String, Integer

from .database import Base


class Recipes(Base):
    __tablename__ = "Recipes"
    recipe_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number_views = Column(Integer, default=0, index=True)
    cooking_time = Column(Integer, index=True)


class DeepRecipes(Base):
    __tablename__ = "DeepRecipes"
    recipe_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ingredients = Column(String)
    description = Column(String)
