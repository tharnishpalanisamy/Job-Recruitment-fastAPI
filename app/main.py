from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
app.include_router(v1_router)
