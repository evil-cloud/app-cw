import logging
import json
import sys
from src.core.config import settings
from datetime import datetime, timezone
import os

class BaseJSONFormatter(logging.Formatter):
    """
    Formateador base JSON con timestamp y nivel.
    """
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat() + "Z"

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict):
            log_entry.update(record.extra_data)
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

class DetailedJSONFormatter(logging.Formatter):
    """
    Formateador JSON detallado con informacion de la ubicacion del log.
    """
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat() + "Z"

    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "module": record.module,
            "funcName": record.funcName,
            "pathname": record.pathname,
            "lineno": record.lineno
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict):
            log_entry.update(record.extra_data)
        
        return json.dumps(log_entry)

def setup_logging():
    """
    Configura el logger de la aplicacion para usar diferentes formatos JSON
    y escribir en un archivo y consola.
    """
    log_level = settings.LOG_LEVEL
    log_file_path = settings.LOG_FILE_PATH

    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(settings.SERVICE_NAME) 
    logger.setLevel(log_level)
    logger.propagate = False 

    if logger.hasHandlers():
        logger.handlers.clear()

    base_formatter = BaseJSONFormatter()
    detailed_formatter = DetailedJSONFormatter()

    formatter_map = {
        logging.DEBUG: detailed_formatter,
        logging.INFO: detailed_formatter,
        logging.WARNING: base_formatter,
        logging.ERROR: base_formatter,
        logging.CRITICAL: base_formatter,
    }

    class CustomLevelFormatter(logging.Formatter):
        """
        Selecciona el formateador basado en el nivel del log y maneja los 'extra' data.
        """
        def format(self, record):
            if isinstance(record.args, dict) and 'extra' in record.args:
                record.extra_data = record.args['extra']
                record.args = () 
            else:
                record.extra_data = {}

            if record.levelno in formatter_map:
                return formatter_map[record.levelno].format(record)
            return base_formatter.format(record)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(CustomLevelFormatter())
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomLevelFormatter())
    logger.addHandler(console_handler)

    logger.info(f"Logging configurado para nivel {log_level}. Logs se escribiran en: {log_file_path} y consola.")
    return logger

app_logger = setup_logging()