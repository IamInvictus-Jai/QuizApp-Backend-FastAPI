from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.settings import get_settings, Settings
from .middlewares.globalExceptionHandlers import ExceptionMiddleware
from .utils.addRoutes import add_routes
from .dependency.container import Container
import mongoengine

def init_app(app: FastAPI, settings: Settings) -> None:
    container = Container()

    # Store container reference in app
    app.container = container

    try:
        container.logger().info("Initializing container and resources...")

        # Connect to database
        database = settings.MONGO_DATABASE_NAME
        host = settings.MONGO_DATABASE_HOST
        mongoengine.connect(db=database, host=host)

        container.wire(
            modules=[
                "app.middlewares.globalExceptionHandlers",
            ],
            packages=[
                "app.api.v1",
            ]
        )
        container.logger().info("Container wired and resources initialized\n\n")
    except Exception as e:
        container.logger().error(f"Startup failed: {str(e)}")
        raise RuntimeError(f"Failed to initialize: {str(e)}")

def create_app() -> FastAPI:
    settings = get_settings()

    # Create FastAPI instance
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )


    # Add startup and shutdown events
    init_app(app, settings)

    # Set up CORS and exception middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )
    app.add_middleware(ExceptionMiddleware)

    # Add Routers
    add_routes(app)

    return app


app = create_app()