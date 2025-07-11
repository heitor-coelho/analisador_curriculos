from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Query
from fastapi.concurrency import run_in_threadpool
from typing import List, Optional
from uuid import UUID
from app.services.analyze_service import process_files
from app.services.log_service import LogService

router = APIRouter()

@router.post("/")
async def analyze_curriculums(
    files: List[UploadFile] = File(...),
    query: Optional[str] = Form(None),
    request_id: UUID = Form(...),
    user_id: str = Form(...)
):
    try:
        processed_result = await run_in_threadpool(process_files, files, query)
    except Exception as e:
        # Log de erro
        await LogService.save_log(
            request_id=str(request_id),
            user_id=user_id,
            query=query if query else "",
            status="error",
            error_message=str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar os arquivos: {e}"
        )

    # Resultado OK
    if query:
        result = {
            "message": "Análise concluída! Encontramos os currículos mais alinhados com sua busca.",
            "ranked_resumes": processed_result.get("ranked_results"),
        }
    else:
        result = {
            "message": "Extraímos o resumo dos currículos para você, facilitando a leitura rápida.",
            "all_resumes": processed_result.get("all_resumes"),
        }

    # Salvar log do sucesso
    await LogService.save_log(
        request_id=str(request_id),
        user_id=user_id,
        query=query,
        result=result,
    )

    return {
        "request_id": str(request_id),
        "user_id": user_id,
        "query": query,
        "result": result
    }



