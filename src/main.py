from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID, uuid4
from postgrest.exceptions import APIError

from src.config import logger
from src.cv_processing.router import router as cv_processing_router
from src.users.router import router as users_router
from src.exceptions import APIException

# Inicialización de la aplicación FastAPI.
app = FastAPI(
    title="API de Procesamiento de CVs",
    description="Una API para extraer información de currículums de forma asíncrona usando IA.",
    version="2.0.0",
)

# Exception Handler
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(cv_processing_router)
app.include_router(users_router, prefix="/users")

@app.get("/", summary="Endpoint de Bienvenida")
async def read_root():
    """Devuelve un mensaje de bienvenida para verificar que la API está activa."""
    logger.info("Solicitud recibida en el endpoint de bienvenida.")
    return {"message": "Bienvenido a la API de Procesamiento de CVs"}

