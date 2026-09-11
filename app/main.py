from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.config import settings

app = FastAPI(title=settings.app_name)

app.include_router(upload_router)
