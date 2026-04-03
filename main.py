from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.models import Base
from app.api.v1 import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}