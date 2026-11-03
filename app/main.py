from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.core import setup_logging
from app.exception_handlers import register_exception_handlers
from app.middleware import logging_middleware

setup_logging()
app = FastAPI()

app.middleware("http")(logging_middleware)
register_exception_handlers(app)
app.include_router(v1_router)
