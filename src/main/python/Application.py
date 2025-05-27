from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.main.python.config.DatabasesConfig import engine
from src.main.python.models.Profile import Base
from src.main.python.controller.ProfileController import router as profile_router
from src.main.python.controller.FollowController import router as follower_router
from src.main.python.controller.IngredientController import router as ingredient_router
from src.main.python.controller.IngredientAllergyController import router as allergy_router
from src.main.python.controller.ShoppingListController import router as shopping_list_router
from src.main.python.controller.SavedRecipeController import router as saved_recipe_router

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="Profile Microservice")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(profile_router)
    app.include_router(follower_router)
    app.include_router(ingredient_router)
    app.include_router(allergy_router)
    app.include_router(shopping_list_router)
    app.include_router(saved_recipe_router)

    return app

app = create_app()
