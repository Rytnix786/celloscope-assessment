from fastapi import FastAPI

from api.router import api_router

app = FastAPI(
    title="Speech & Document Extraction API",
    description="Celloscope Take-Home Service",
    version="0.1.0",
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    from config import settings

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
