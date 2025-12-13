import logging
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from supabase import create_client, Client
from pathlib import Path # Nueva importación


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
    exit(1)

# Inicialización de Supabase
try:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Error: Supabase URL o Key no configurados en .env")
        # Considerar elevar una excepción o salir en entornos de producción.
        exit(1)

    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except ImportError:
    logger.error(
        "Error: La librería 'supabase' no está instalada. Por favor, ejecuta 'pip install supabase'"
    )
    exit(1)
except Exception as e:
    exit(1)

# Costo en créditos por cada procesamiento de CV
CREDIT_COST = 100
