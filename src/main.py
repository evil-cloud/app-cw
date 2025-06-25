from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import datetime
import json
import logging
import sys
import traceback
import uuid
from src.core.config import settings
from src.core.logging_config import setup_logging
from fastapi import HTTPException

logger = setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API de demostracion para filtros de metricas de CloudWatch con logs JSON.",
    docs_url="/docs",
    redoc_url="/redoc"
)

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.datetime.utcnow()
        response = await call_next(request)
        process_time_seconds = (datetime.datetime.utcnow() - start_time).total_seconds()
        process_time_ms = int(process_time_seconds * 1000)

        if request.url.path not in ["/health", "/docs", "/redoc", "/openapi.json"]:
            log_data = {
                "app_name": settings.SERVICE_NAME,
                "request_method": request.method,
                "request_path": request.url.path,
                "response_status_code": response.status_code,
                "process_time_ms": process_time_ms,
                "client_ip": request.client.host if request.client else "unknown"
            }

            if 400 <= response.status_code < 500:
                logger.warning("Solicitud de cliente procesada con advertencia.", extra=log_data)
            elif response.status_code >= 500:
                logger.error("Solicitud de cliente procesada con error del servidor.", extra=log_data)
            else:
                logger.info("Solicitud HTTP procesada.", extra=log_data)
        
        return response

app.add_middleware(LogMiddleware)

from src.api.routes import router as api_router
app.include_router(api_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_traceback = traceback.format_exc()
    request_id = str(uuid.uuid4())
    error_data = {
        "app_name": settings.SERVICE_NAME,
        "request_id": request_id, 
        "error_type": "UNHANDLED_EXCEPTION",
        "error_message": str(exc),
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "request_path": str(request.url),
        "traceback": error_traceback
    }
    logger.error("Excepcion no manejada", exc_info=True, extra=error_data) 
    
    public_error_data = {
        "message": "Ocurrio un error inesperado. Por favor, intentalo de nuevo mas tarde.",
        "request_id": request_id 
    }
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=public_error_data)

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found_handler(request: Request, exc):
    request_id = str(uuid.uuid4())
    error_data = {
        "app_name": settings.SERVICE_NAME,
        "request_id": request_id,
        "error_type": "NOT_FOUND",
        "error_message": "El endpoint al que intentas acceder no existe.",
        "status_code": status.HTTP_404_NOT_FOUND,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "request_path": str(request.url)
    }
    logger.info("Endpoint no encontrado.", extra=error_data)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_data)