from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.models import Base
from app.api.v1 import api_router
# App entry point.
# Creates DB tables on startup, registers all routers.
# Run with: uvicorn main:app --reload
Base.metadata.create_all(bind=engine)
# creates all tables that don't exist yet — safe to run multiple times

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(api_router)
# all routes live under /api/v1/

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}

# quick check that the server is up — no auth needed
