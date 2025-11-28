from fastapi import FastAPI, HTTPException
from src.config import logger, supabase_client
from src.cv_processing.router import router as cv_processing_router
from uuid import UUID, uuid4  # Import uuid4 for generating UUIDs
from postgrest.exceptions import APIError


# Inicialización de la aplicación FastAPI.
app = FastAPI(
    title="API de Procesamiento de CVs",
    description="Una API para extraer información de currículums de forma asíncrona usando IA.",
    version="2.0.0",
)

# Incluir routers
app.include_router(cv_processing_router)


@app.get("/", summary="Endpoint de Bienvenida")
async def read_root():
    """Devuelve un mensaje de bienvenida para verificar que la API está activa."""
    logger.info("Solicitud recibida en el endpoint de bienvenida.")
    return {"message": "Bienvenido a la API de Procesamiento de CVs"}
