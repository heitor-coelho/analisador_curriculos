from datetime import datetime
from typing import Optional
import traceback

from app.repository.log_repository import LogRepository

class LogService:
    @staticmethod
    async def save_log(
        *,
        request_id: str,
        user_id: str,
        query: str,
        result: Optional[dict] = None,
        status: str = "success",
        error_message: Optional[str] = None,
        **kwargs
    ):
        try:
            existing_log = await LogRepository.find_by_request_id(request_id)
            if existing_log:
                print(f"Log para request_id {request_id} já existe. Ignorando.")
                return

            log_data = {
                "request_id": request_id,
                "user_id": user_id,
                "query": query,
                "timestamp": datetime.utcnow(),
                "status": status,
                "result": result if status == "success" else None,
                "error_message": error_message if status == "error" else None,
                **kwargs
            }

            await LogRepository.insert_log(log_data)
            print(f"Log salvo com sucesso para request_id {request_id}")

        except Exception as e:
            print(f"[ERRO AO SALVAR LOG] {e}")
            traceback.print_exc()

    @staticmethod
    async def get_logs(user_id: Optional[str] = None, request_id: Optional[str] = None):
        try:
            return await LogRepository.find_logs(user_id=user_id, request_id=request_id)
        except Exception as e:
            print(f"[ERRO AO BUSCAR LOGS] {e}")
            traceback.print_exc()
            return []
