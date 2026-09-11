from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.health import router as health_router
from app.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
