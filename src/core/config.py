import os

class Settings:
    """
    Clase para gestionar la configuracion de la aplicacion desde variables de entorno.
    """
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "CloudWatch Metrics Filter Demo API")
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "cw-api")
    VERSION: str = "1.0.0"

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", "/var/log/cw-api/logs.json")

    API_PORT: int = int(os.getenv("API_PORT", 80))

settings = Settings()