from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.database import Base, engine
from app.routers import atleta as atleta_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Workout API - Crossfit",
    version="1.0.0",
)

app.include_router(atleta_router.router)

add_pagination(app)
