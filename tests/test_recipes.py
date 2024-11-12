def test_get_all_recipes(client):
    response = client.get("/recipes/")
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_new_recipe(client):
    new_recipe_data = {"name": "Пельмени", "number_views": 0, "cooking_time": 20}
    response = client.post("/recipes", json=new_recipe_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "Пельмени"


def test_get_recipe_by_id(client):
    response = client.get("/recipes/1")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "Пельмени"


def test_create_existing_recipe(client):
    existing_recipe_data = {"name": "Пельмени", "number_views": 0, "cooking_time": 20}
    response = client.post("/recipes", json=existing_recipe_data)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Этот рецепт уже существует."


def test_add_ingredients(client):
    ingredients_data = {
        "name": "Пельмени",
        "ingredients": "Тесто, фарш",
        "description": "Пельмени домашние",
    }
    response = client.post("/deep_recipes?recipe_id=1", json=ingredients_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "Пельмени"
    assert response.json()["ingredients"] == "Тесто, фарш"


def test_add_existing_deep_recipe(client):
    ingredients_data = {
        "name": "Пельмени",
        "ingredients": "Тесто, фарш",
        "description": "Пельмени домашние",
    }
    response = client.post("/deep_recipes?recipe_id=1", json=ingredients_data)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Этот рецепт уже существует."
