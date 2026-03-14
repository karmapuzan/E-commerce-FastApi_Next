from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.routes.public import auth
from src.db.database import create_table
from src.core.config import settings

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

# Public route
app.include_router(
    auth.router,
    prefix=f"{settings.API_PREFIX}",
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
