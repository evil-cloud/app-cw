from fastapi import APIRouter, HTTPException, status
from src.services.cw_logic import process_success_request, process_error_request
from src.models.schemas import SuccessResponse, ErrorResponse, HealthResponse
from src.core.config import settings
from typing import Union

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint de salud de la aplicacion.
    """
    return {
      "status": "ok", 
      "service_name": settings.SERVICE_NAME, 
      "version": settings.VERSION
    }

@router.get("/api/v1/cw/success", response_model=SuccessResponse)
async def get_cw_success():
    """
    Simula una solicitud exitosa y genera un log de INFO.
    """
    response_data = await process_success_request()
    return response_data

@router.get("/api/v1/cw/error", response_model=Union[SuccessResponse, ErrorResponse])
async def get_cw_error(error_type: str = "internal"):
    """
    Simula una solicitud con error y genera un log de WARNING, ERROR o CRITICAL.
    Parametro 'error_type': 'internal', 'not_found', 'random', 'critical'.
    """
    response_data = await process_error_request(error_type)
    return response_data