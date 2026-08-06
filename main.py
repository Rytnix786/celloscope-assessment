import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from api.router import api_router
from config import settings

# Structured logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("celloscope")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(f"Service starting up in ADAPTER_MODE='{settings.ADAPTER_MODE}'")
    yield
    logger.info("Service shutting down")


app = FastAPI(
    title="Speech & Document Extraction API",
    description="Celloscope Take-Home Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
