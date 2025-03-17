from fastapi import FastAPI
from src.main.python.config.DatabasesConfig import engine
from src.main.python.models.Profile import Base
from src.main.python.controller.ProfileController import router as profile_router
from src.main.python.controller.FollowController import router as follower_router
from src.main.python.controller.IngredientController import router as ingredient_router
from src.main.python.controller.RestrictionController import router as restriction_router
from src.main.python.controller.ShoppingListController import router as shopping_list_router

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="Profile Microservice")
    app.include_router(profile_router)
    app.include_router(follower_router)
    app.include_router(ingredient_router)
    app.include_router(restriction_router)
    app.include_router(shopping_list_router)


    return app

app = create_app()
