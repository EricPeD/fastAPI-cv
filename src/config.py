import logging
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from supabase import Client, create_async_client
from pathlib import Path # Nueva importación
from typing import Optional


# --- Configuración Inicial ---
load_dotenv()

# Configuración de directorio y archivo de logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True) # Asegura que el directorio 'logs' exista
LOG_FILE_PATH = LOG_DIR / "app.log"

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOG_FILE_PATH, # Guardar logs en un archivo
    filemode='a' # Anexar logs si el archivo ya existe
)
logger = logging.getLogger(__name__)

# Instancia de OpenAI
try:
    openai_client = AsyncOpenAI()
except Exception as e:
    logger.error(f"Error al inicializar el cliente de OpenAI: {e}")
    raise Exception(f"Error al inicializar el cliente de OpenAI: {e}")

# Declaración de Supabase Client (se inicializará en el evento de startup de FastAPI)
_supabase_client_instance: Optional[Client] = None

def set_supabase_client(client: Client):
    global _supabase_client_instance
    _supabase_client_instance = client

def get_supabase_client() -> Client:
    if _supabase_client_instance is None:
        raise RuntimeError("Supabase client has not been initialized.")
    return _supabase_client_instance
