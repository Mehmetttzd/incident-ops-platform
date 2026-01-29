from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.incidents import router as incidents_router


app = FastAPI(
    title="Incident Ops Intelligence Platform",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(incidents_router)