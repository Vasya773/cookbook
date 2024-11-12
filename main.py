from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy import and_

from .database import Base, async_session, engine, session
from .models import Recipes, DeepRecipes
from .schemas import RecipesOut, RecipesIn, DeepRecipesOut, DeepRecipesIn
import uvicorn


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/recipes/", response_model=List[RecipesOut])
async def get_all_recipes() -> List[Recipes]:
    """Получение всех рецептов из кулинарной книги"""
    async with async_session() as session:
        res = await session.execute(
            select(Recipes).order_by(Recipes.number_views.desc(), Recipes.cooking_time)
            )
        return res.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=RecipesOut)
async def get_recipe_by_id(recipe_id: int):
    """Получение детальной информации о конкретном рецепте по ID"""
    async with async_session() as session:
        result = await session.execute(
            select(Recipes).where(Recipes.recipe_id == recipe_id)
        )
        recipe = result.scalar_one_or_none()

        if recipe is None:
            raise HTTPException(status_code=404, detail="Рецепт не найден")

        recipe.number_views += 1
        await session.commit()
        return RecipesOut.from_orm(recipe)


@app.post("/recipes", response_model=RecipesOut)
async def create_new_recipe(recipes: RecipesIn):
    """Создание нового рецепта"""
    async with async_session() as session:
        new_recipe = Recipes(**recipes.dict())

        existing_recipe = await session.execute(
            select(Recipes).where(Recipes.name == recipes.name
            )
        )
        result_existing_recipe = existing_recipe.scalar_one_or_none()

        if result_existing_recipe is not None:
            raise HTTPException(status_code=400, detail="Этот рецепт уже существует.")

        session.add(new_recipe)
        await session.commit()
        await session.refresh(new_recipe)
        return RecipesOut.from_orm(new_recipe)


@app.post("/deep_recipes", response_model=DeepRecipesOut)
async def add_ingredients(recipe_id: int, deep_recipe: DeepRecipesIn):
    """Добавление ингредиентов для создания блюда"""
    async with async_session() as session:
        result = await session.execute(
            select(Recipes).where(Recipes.recipe_id == recipe_id)
        )
        recipe = result.scalar_one_or_none()

        if recipe is None:
            raise HTTPException(status_code=404, detail="Рецепт не найден")

        existing_deep_recipe = await session.execute(
            select(DeepRecipes).where(
                and_(
                    DeepRecipes.name == recipe.name,
                    DeepRecipes.ingredients == deep_recipe.ingredients
                )
            )
        )
        result_existing_deep_recipe = existing_deep_recipe.scalar_one_or_none()

        if result_existing_deep_recipe is not None:
            raise HTTPException(status_code=400, detail="Этот рецепт уже существует.")


        new_deep_recipes = DeepRecipes(
            name=recipe.name,
            ingredients=deep_recipe.ingredients,
            description=deep_recipe.description,
        )
        session.add(new_deep_recipes)
        await session.commit()
        return DeepRecipesOut.from_orm(new_deep_recipes)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
