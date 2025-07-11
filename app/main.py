from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router

from app.db.mongo import connect_mongo, close_mongo



app = FastAPI(
    title="API de Análise de Currículos",
    description="Processamento e ranqueamento de currículos via LLM/OCR.",
    version="1.0.0"
)

app.include_router(api_router)  

@app.on_event("startup")
async def startup_db_client():
    await connect_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    close_mongo()

