import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import engine
from app.routes import admin_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_logger")

# test database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Checking MySQL database connection...")
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("Successfully connected to the MySQL database! yeay")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    yield

app = FastAPI(lifespan=lifespan)

# test api response
@app.get("/")
async def root():
    return {"message": "Ping pong!"}

app.include_router(admin_router.router)