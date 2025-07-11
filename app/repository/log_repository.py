from app.db.mongo import logs_collection
from typing import Optional, Dict, Any
from datetime import datetime

class LogRepository:
    @staticmethod
    async def find_by_request_id(request_id: str) -> Optional[dict]:
        return await logs_collection.find_one({"request_id": request_id})

    @staticmethod
    async def insert_log(log_data: Dict[str, Any]):
        await logs_collection.insert_one(log_data)

    @staticmethod
    async def find_logs(user_id: Optional[str] = None, request_id: Optional[str] = None):
        query = {}
        if user_id:
            query["user_id"] = user_id
        if request_id:
            query["request_id"] = request_id

        cursor = logs_collection.find(query).sort("timestamp", -1)
        logs = []
        async for log in cursor:
            log["_id"] = str(log["_id"])
            logs.append(log)
        return logs
