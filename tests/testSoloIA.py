import asyncio
import os
import json
import logging
import base64
import mimetypes

from src.config import logger, openai_client
from src.models import CVInfo

# Usamos el logger configurado en la app
logger = logging.getLogger(__name__)

async def extract_cv_info_from_file(file_path: str) -> CVInfo | None:
    """
    Envía un archivo (imagen o PDF como imagen) a GPT-4o y extrae la información del CV.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY":
        logger.error("Error: La clave de API de OpenAI no está configurada.")
        return None

    if not os.path.exists(file_path):
        logger.error(f"Archivo de prueba no encontrado: {file_path}")
        return None

    try:
        # Leer el archivo como bytes
        with open(file_path, "rb") as file:
            file_content = file.read()
        
        # Codificar el contenido del archivo a base64
        base64_content = base64.b64encode(file_content).decode('utf-8')
        
        # Determinar el MIME type del archivo
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream" # Fallback
            logger.warning(f"No se pudo determinar el MIME type para {file_path}, usando fallback.")

    except Exception as e:
        logger.exception(f"Error al leer o codificar el archivo de prueba: {e}")
        return None

    system_prompt = """
    Eres un experto en reclutamiento y análisis de currículums.
    Analiza la imagen del CV que se te proporciona y extrae toda la información relevante.
    Devuelve ÚNICAMENTE un JSON válido con esta estructura exacta:

    {
        "name": "string o null",
        "email": "string o null",
        "phone": "string o null",
        "resumen": "string o null",
        "experiencia": [
            {
                "puesto": "string",
                "empresa": "string",
                "periodo": "string",
                "descripcion": "string"
            }
        ],
        "educacion": [
            {
                "titulo": "string",
                "institucion": "string",
                "periodo": "string"
            }
        ],
        "habilidades": ["string"],
        "soft_skills": ["string"]
    }

    - Usa listas vacías [] si no hay datos en experiencia, educación, habilidades, etc.
    - El nombre y el email son campos críticos. Intenta siempre extraerlos.
    - El JSON debe ser 100% válido y parseable.
    """

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extrae toda la información de este CV en formato JSON exacto."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_content}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=2000
        )

        json_text = response.choices[0].message.content.strip()
        
        # Limpieza adicional por si acaso
        if json_text.startswith("```json"):
            json_text = json_text[7:-3].strip()
        elif json_text.startswith("```"):
            json_text = json_text[3:-3].strip()

        extracted_data = json.loads(json_text)
        extracted_data["full_text"] = "(Texto extraído de la imagen por IA)"
        extracted_data["source_file"] = os.path.basename(file_path)

        return CVInfo(**extracted_data)

    except json.JSONDecodeError as e:
        logger.error(f"Error: La IA devolvió JSON inválido:\n{json_text}\nError: {e}")
        return None
    except Exception as e:
        logger.exception(f"Error al procesar el CV con OpenAI: {e}")
        return None

async def main():
    """
    Función principal para ejecutar la extracción del CV y mostrar el resultado.
    """
    test_cv_path = "testCV/cv/CV_Nicolas_Penuela.png"
    
    print(f"Iniciando extracción del CV '{test_cv_path}' usando la API de OpenAI...")
    result = await extract_cv_info_from_file(test_cv_path)
    
    if result:
        print("\n--- Resultado de la Extracción ---")
        # Usamos ensure_ascii=False para que muestre correctamente los caracteres como 'ñ'
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
        print("----------------------------------")
    else:
        print(f"\nNo se pudo extraer información del CV '{test_cv_path}'. Revisa los logs para más detalles.")

if __name__ == "__main__":
    asyncio.run(main())