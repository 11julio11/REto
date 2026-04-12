import logging
import sys
import os

# Añadir el path para que encuentre src
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from src.config.observability import setup_logging, trace_id_var

def test_json_logging():
    setup_logging()
    logger = logging.getLogger("test_logger")
    
    # Simular una petición con trace_id
    token = trace_id_var.set("test-trace-123")
    try:
        logger.info("Verificando logs JSON con trace_id")
    finally:
        trace_id_var.reset(token)
        
    logger.info("Verificando logs JSON sin trace_id")

if __name__ == "__main__":
    test_json_logging()
