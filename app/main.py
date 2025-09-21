from fastapi import FastAPI, Response, Depends
from contextlib import asynccontextmanager
from app.core.config import Settings, get_settings, get_project_version, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=get_project_version(),
    lifespan=lifespan,
)


@app.get("/")
def read_root(
        settings: Settings = Depends(get_settings),
):
    return {
        "message": "Welcome to {settings.APP_NAME}!}",
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        "database_host": settings.DB.HOST,
        "database_url_hidden_password": settings.DB.DATABASE_URL.replace(
            settings.DB.PASSWORD, "*****"
        ),
        "app-version": get_project_version(),
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}

