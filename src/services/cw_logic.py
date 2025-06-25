import uuid
import random
from src.core.logging_config import app_logger
from fastapi import HTTPException, status
from src.core.config import settings

async def process_success_request():
    """
    Simula una operación exitosa y genera un log de éxito.
    """
    request_id = str(uuid.uuid4())
    duration_ms = random.randint(50, 200)

    app_logger.info(
        "Solicitud procesada exitosamente.",
        extra={
            "app_name": settings.SERVICE_NAME,
            "request_id": request_id,
            "status": "SUCCESS",
            "endpoint": "/api/v1/cw/success",
            "duration_ms": duration_ms
        }
    )
    return {
        "message": "Operación exitosa",
        "request_id": request_id,
        "app_name": settings.SERVICE_NAME,
        "status": "SUCCESS",
        "endpoint": "/api/v1/cw/success",
        "duration_ms": duration_ms
    }

async def process_error_request(error_type: str):
    """
    Simula una operación con fallo o éxito según el tipo de error.
    - error_type: 'internal' (default), 'not_found', 'random', 'critical'
    """
    request_id = str(uuid.uuid4())
    duration_ms = random.randint(300, 800)

    valid_error_types = ["internal", "not_found", "random", "critical"]
    if error_type not in valid_error_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": f"Tipo de error no válido: '{error_type}'. Tipos permitidos: {', '.join(valid_error_types)}.",
                "app_name": settings.SERVICE_NAME,
                "request_id": request_id,
                "status": "INVALID_INPUT",
                "error_code": "INVALID_ERROR_TYPE",
                "endpoint": "/api/v1/cw/error",
                "duration_ms": duration_ms
            }
        )

    if error_type == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Recurso no encontrado.",
                "app_name": settings.SERVICE_NAME,
                "request_id": request_id,
                "status": "NOT_FOUND",
                "error_code": "RESOURCE_NOT_FOUND",
                "endpoint": "/api/v1/cw/error",
                "duration_ms": duration_ms
            }
        )
    
    elif error_type == "random":
        if random.random() < 0.5:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Ocurrió un error aleatorio al procesar la solicitud.",
                    "app_name": settings.SERVICE_NAME,
                    "request_id": request_id,
                    "status": "FAILURE",
                    "error_code": "SIMULATED_RANDOM_ERROR",
                    "endpoint": "/api/v1/cw/error",
                    "duration_ms": duration_ms
                }
            )
        else:
            duration_ms = random.randint(50, 200)
            app_logger.info(
                "Solicitud aleatoria exitosa (a pesar de ser el endpoint de error).",
                extra={
                    "app_name": settings.SERVICE_NAME,
                    "request_id": request_id,
                    "status": "SUCCESS",
                    "endpoint": "/api/v1/cw/error",
                    "duration_ms": duration_ms
                }
            )
            return {
                "message": "Operación aleatoria exitosa",
                "request_id": request_id,
                "app_name": settings.SERVICE_NAME,
                "status": "SUCCESS",
                "endpoint": "/api/v1/cw/error",
                "duration_ms": duration_ms
            }

    elif error_type == "critical":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Un error crítico simulado ha ocurrido.",
                "app_name": settings.SERVICE_NAME,
                "request_id": request_id,
                "status": "CRITICAL_FAILURE",
                "error_code": "SIMULATED_CRITICAL_ERROR",
                "endpoint": "/api/v1/cw/error",
                "duration_ms": duration_ms
            }
        )

    else: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Ocurrió un error interno inesperado al procesar la solicitud.",
                "app_name": settings.SERVICE_NAME,
                "request_id": request_id,
                "status": "FAILURE",
                "error_code": "INTERNAL_SERVER_ERROR",
                "endpoint": "/api/v1/cw/error",
                "duration_ms": duration_ms
            }
        )