from typing import Annotated
from fastapi import Depends
from dependency_injector.wiring import Provide

from logging import Logger
from app.config.settings import Settings
from app.dependency.container import Container
from app.services.notesService import NotesService
from app.services.quizService import QuizService

class Dependencies:
    """
    Central dependency management class that defines type-safe dependencies
    for dependency injection throughout the application.
    """
    LoggerDependency = Annotated[Logger, Depends(Provide[Container.logger])]
    SettingsDependency = Annotated[Settings, Depends(Provide[Container.settings])]
    NotesServiceDependency = Annotated[NotesService, Depends(Provide[Container.notes_service])]
    QuizServiceDependency = Annotated[QuizService, Depends(Provide[Container.quiz_service])]

    