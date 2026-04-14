import logging
import sys
import uuid
from contextvars import ContextVar
from pythonjsonlogger import jsonlogger
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

# Contexto para almacenar el trace_id de la petición actual
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="n/a")

class TraceIdFilter(logging.Filter):
    """Filtro que inyecta el trace_id del contexto en cada registro de log."""
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        return True

class TracingMiddleware(BaseHTTPMiddleware):
    """Middleware que genera un Trace ID por petición y lo añade a los headers."""
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        token = trace_id_var.set(trace_id)
        try:
            response = await call_next(request)
            response.headers["X-Trace-Id"] = trace_id
            return response
        finally:
            trace_id_var.reset(token)

def setup_logging():
    """Configura el logging standar de Python para que use formato JSON."""
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.addFilter(TraceIdFilter()) # Inyectar trace_id
    
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(severity)s %(name)s %(message)s %(trace_id)s',
        rename_fields={'levelname': 'severity', 'asctime': 'timestamp'}
    )
    
    log_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.INFO)

def setup_metrics(app: FastAPI):
    """Inicializa Prometheus Instrumentator para exponer métricas en /metrics."""
    Instrumentator().instrument(app).expose(app)


