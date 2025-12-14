import os
import json
import base64
import io
import mimetypes
from pathlib import Path
from PIL import Image
import fitz

from src.config import logger, openai_client
from src.exceptions import OpenAIError

async def extract_info_with_openai_vision(file_path: Path, output_schema: dict) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado para OpenAI Vision: {file_path}")

    messages_content = [{"type": "text", "text": "Extrae toda la información de este archivo en formato JSON exacto."}]
    
    mime_type, _ = mimetypes.guess_type(file_path.name)
    
    if mime_type == "application/pdf":
        try:
            document = fitz.open(file_path)
            for page_num, page in enumerate(document):
                if page_num >= 10:
                    logger.warning(f"CV {file_path.name} tiene más de 10 páginas. Solo se procesarán las primeras 10.")
                    break
                pix = page.get_pixmap()
                img_bytes = io.BytesIO()
                Image.frombytes("RGB", [pix.width, pix.height], pix.samples).save(img_bytes, format="PNG")
                base64_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
                messages_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}
                })
            document.close()
            if len(messages_content) == 1:
                raise OpenAIError(f"No se pudo extraer ninguna imagen de las páginas del PDF {file_path.name}.")
        except Exception as e:
            raise OpenAIError(f"Error al procesar PDF para OpenAI Vision {file_path.name}: {e}")
    elif mime_type and mime_type.startswith("image/"):
        try:
            with open(file_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            messages_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}", "detail": "high"}
            })
        except Exception as e:
            raise OpenAIError(f"Error al procesar imagen para OpenAI Vision {file_path.name}: {e}")
    else:
        raise OpenAIError(f"Tipo de archivo no soportado para OpenAI Vision: {mime_type} en {file_path.name}")
    
    schema_string = json.dumps(output_schema, indent=2, ensure_ascii=False)
    system_prompt = f"""
    Eres un agente de IA autónomo especializado en el análisis de documentos. Tu objetivo es procesar el siguiente documento y extraer la información solicitada en un formato JSON estricto.
    ESQUEMA DE SALIDA REQUERIDO (DEBES SEGUIRLO ESTRICTAMENTE):
    {schema_string}
    REGLAS ADICIONALES:
    - Tu respuesta debe ser ÚNICAMENTE el objeto JSON puro y válido. No incluyas texto introductorio, comentarios, ni bloques de código.
    """
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": messages_content}],
            response_format={"type": "json_object"},
            max_tokens=2048,
        )
        json_text = response.choices[0].message.content.strip()
        return json.loads(json_text)
    except Exception as e:
        logger.exception(f"Error al procesar el CV con OpenAI Vision: {e}")
        raise OpenAIError("Error en la llamada a la API de OpenAI Vision.")

async def extract_info_from_text_with_openai(text: str, output_schema: dict) -> dict:
    if not text:
        raise ValueError("El texto de entrada no puede estar vacío.")

    schema_string = json.dumps(output_schema, indent=2, ensure_ascii=False)
    system_prompt = f"""
    Eres un agente de IA autónomo. Tu objetivo es procesar el siguiente texto y extraer la información solicitada en un formato JSON estricto.
    ESQUEMA DE SALIDA REQUERIDO (DEBES SEGUIRLO ESTRICTAMENTE):
    {schema_string}
    REGLAS ADICIONALES:
    - Tu respuesta debe ser ÚNICAMENTE el objeto JSON puro y válido.
    """
    user_prompt = f"Analiza el siguiente texto y extrae la información en el formato JSON especificado:\n---\n{text}"

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-5-nano",
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.exception(f"Error en la API de OpenAI (texto): {e}")
        raise OpenAIError("Error en la llamada a la API de OpenAI (texto).")
