from dependency_injector import containers, providers
from app.config.settings import get_settings
from app.core.logger import get_logger
from app.utils.readInstructions import LoadInstructions
from app.core.LLM import LLM
from app.services.notesService import NotesService
from app.services.quizService import QuizService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
                "app.middlewares.globalExceptionHandlers",
            ],
        packages=[
            "app.api.v1",
        ]
    )

    # Singletons
    settings = providers.Singleton(get_settings)
    logger = providers.Singleton(get_logger, "app", "app/logs")
    load_instructions = providers.Singleton(LoadInstructions, base_filename="app/system_instructs")
    llm = providers.Singleton(LLM, load_instructions, settings)
    notes_service = providers.Singleton(NotesService, logger, load_instructions, llm)
    quiz_service = providers.Singleton(QuizService, logger, load_instructions, llm)
    