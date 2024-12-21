from typing import Union, Optional, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from json import loads, dumps

from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

class Recipe(BaseModel):
    name: str
    ingredients: list[Item]
    procedure: str
    taste: str
    cuisine_type: str
    duration: str

file = "db.json"

def read_db():
    with open(file) as f:
        return f.read()

def write_db(data):
    with open(file, "w") as f:
        f.write(data)

def create_recipe(recipe: Recipe):
    data = loads(read_db())
    data["recipes"].append(recipe)
    write_db(dumps(data))

def read_recipe(name: str):
    data = loads(read_db())
    found = {}
    for recipe in data["recipes"]:
        if recipe["name"] == name:
            found = recipe
            break
    return recipe

def read_recipes(recipe: Recipe):
    data = loads(read_db())
    return data["recipes"]

def update_recipe(recipe: Recipe):
    data = loads(read_db())
    found = {}
    for i, recipe in enumerate(data["recipes"]):
        if recipe["name"] == name:
            data["recipes"][i] = recipe
            write_db(data)
            break

def remove_recipe(recipe: Recipe):
    for recipe in data["recipes"]:
        if recipe["name"] == name:
            data["recipes"].remove(recipe)
            break

def create_item(item: Item):
    data = loads(read_db())
    data["items"].append(item)
    write_db(dumps(data))

def read_item(name: str):
    data = loads(read_db())
    found = {}
    for item in data["items"]:
        if item["name"] == name:
            found = item
            break
    return item

def read_items(item: Item):
    data = loads(read_db())
    return data["items"]

def update_item(item: Item):
    data = loads(read_db())
    found = {}
    for i, item in enumerate(data["items"]):
        if item["name"] == name:
            data["items"][i] = item
            write_db(data)
            break

def remove_item(item: Item):
    for item in data["items"]:
        if item["name"] == name:
            data["items"].remove(item)
            break

def create_prompt():
    pass

def chat(query: str) -> Recipe:
    pass

def msg(msg: str):
    return { "message" : msg}


# Mount static files directory for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recipe")
def post_recipe(recipe: Recipe):
    create_recipe(recipe)
    return msg("Recipe was created")


@app.get("/recipes")
def get_receipe() -> list[Recipe]:
    recipes = read_recipes()
    return recipes

@app.put("/recipe")
def put_recipe(name: str, recipe: Recipe):
    update_recipe(recipe)
    return msg("Recipe was updated")

@app.delete("/recipe")
def delete_recipe(recipe: Recipe):
    remove_recipe(recipe)
    return msg("Recipe was deleted")


@app.post("/kitchen")
def post_items(items: list[Item]):
    create_item(item)
    return msg("Item is created")


@app.get("/kitchen")
def get_item() -> list[Item]:
    items = read_items()
    return items

@app.put("/kitchen")
def put_items(item: Item):
    update_item(name, item)
    return item

@app.delete("/kitchen")
def delete_items(name: str):
    remove_item(name)
    return msg("Item was deleted")


@app.post("/chat")
def chat_receipe(query: str) -> List[Recipe]:
    response = chat(query)
    return {"response": response}