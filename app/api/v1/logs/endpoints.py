from fastapi import APIRouter
from fastapi import Query
from typing import  Optional
from app.services.log_service import LogService


router = APIRouter()

@router.get("/logs", summary="Listar logs de uso", description="Retorna logs da ferramenta com base no usuário ou request_id.")
async def get_logs(
    user_id: Optional[str] = Query(None, description="Filtrar pelo ID do usuário."),
    request_id: Optional[str] = Query(None, description="Filtrar pelo ID da requisição."),
):
    logs = await LogService.get_logs(user_id=user_id, request_id=request_id)
    return {"logs": logs}