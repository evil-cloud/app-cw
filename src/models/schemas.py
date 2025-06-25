from pydantic import BaseModel
from typing import Optional

class SuccessResponse(BaseModel):
    message: str
    request_id: str
    app_name: str
    status: str
    endpoint: str
    duration_ms: int

class ErrorResponse(BaseModel):
    message: str
    request_id: str
    app_name: str
    status: str
    error_code: str
    endpoint: str
    duration_ms: int
    details: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service_name: str
    version: str
