from fastapi import FastAPI

# Routers
from app.api.health.server import server_health_router
from app.api.v1.notes import notes_router
from app.api.v1.quizes import quiz_router


def add_routes(app: FastAPI) -> None:
    app.include_router(server_health_router)
    app.include_router(notes_router)
    app.include_router(quiz_router)
