from fastapi import FastAPI
from app.routers import routes

app = FastAPI(
    title="FastAPI System",
    description="""A simple FastAPI application.""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(routes.router)