from app.db.mongo import db
import datetime
from typing import Optional, Any

async def save_log(
    request_id: str,
    user_id: str,
    query: Optional[str],
    result: Any
):
    log_doc = {
        "request_id": request_id,
        "user_id": user_id,
        "query": query,
        "result": result,
        "timestamp": datetime.datetime.utcnow()
    }
    inserted = await db.logs.insert_one(log_doc)
    return inserted.inserted_id
