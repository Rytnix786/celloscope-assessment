from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    adapter_mode: str
