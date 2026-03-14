from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.routes.public import category, page
from src.routes.public import auth
from src.db.database import create_table
from src.core.config import settings
from src.routes.protected import (
    page as protected_page,
    category as protected_category,
)

create_table()

app = FastAPI(
    title="Ecommerce API",
    description="An API for an ecommerce website",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public Routes
app.include_router(
    auth.router,
    prefix=f"{settings.API_PREFIX}",
)
app.include_router(page.router, prefix=f"{settings.API_PREFIX}")
app.include_router(category.router, prefix=f"{settings.API_PREFIX}")

# Protected Routes
app.include_router(protected_page.router, prefix=f"{settings.API_PREFIX}")
app.include_router(protected_category.router, prefix=f"{settings.API_PREFIX}")


@app.get("/")
async def root():
    return {"message": "Hello World"}
