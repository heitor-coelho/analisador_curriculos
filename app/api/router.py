# app/api/router.py

from fastapi import APIRouter
from app.api.v1.analyze import endpoints
from app.api.v1.logs import endpoints as log_endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="/analyze", tags=["Análise de Currículos"])
api_router.include_router(log_endpoints.router, prefix="/logs", tags=["Logs de Uso"])
