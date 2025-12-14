from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os # Import os for environment variables
# from uuid import UUID, uuid4 # Not used in main.py, remove if not needed
from postgrest.exceptions import APIError

from src.config import logger, set_supabase_client # Import set_supabase_client
from supabase import create_async_client # Import create_async_client
from src.cv_processing.router import router as cv_processing_router
from src.users.router import router as users_router
from src.exceptions import APIException

# Inicialización de la aplicación FastAPI.
app = FastAPI(
    title="API de Procesamiento de CVs",
    description="Una API para extraer información de currículums de forma asíncrona usando IA.",
    version="2.0.0",
)

# Startup Event
@app.on_event("startup")
async def startup_event():
    try:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.error("Error: Supabase URL o Key no configurados en .env")
            raise Exception("Supabase URL o Key no configurados.")

        client = await create_async_client(SUPABASE_URL, SUPABASE_KEY) # Create and await the async client
        set_supabase_client(client) # Set the client using the config setter
        logger.info("Cliente Supabase asíncrono inicializado correctamente.")
    except ImportError:
        logger.error("Error: La librería 'supabase' no está instalada.")
        raise Exception("Librería 'supabase' no instalada.")
    except Exception as e:
        logger.error(f"Error al inicializar el cliente de Supabase: {e}")
        raise Exception(f"Error al inicializar el cliente de Supabase: {e}")

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

