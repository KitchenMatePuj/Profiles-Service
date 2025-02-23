from fastapi import FastAPI
from src.main.python.config.DatabasesConfig import engine
from src.main.python.models.Profile import Base
from src.main.python.controller.ProfileController import router as profile_router

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(title="Profile Microservice")
    app.include_router(profile_router)
    return app

app = create_app()
