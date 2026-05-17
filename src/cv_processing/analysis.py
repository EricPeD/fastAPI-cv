import os
import json
import base64
import io
import mimetypes
from pathlib import Path
from typing import Tuple
from PIL import Image
import fitz

from src.config import logger, openai_client
from src.exceptions import OpenAIError
from src.models import Usage

# ---------------------------------------------------------------
# Prompt central — se usa igual en vision y en texto
# ---------------------------------------------------------------
def _build_system_prompt(output_schema: dict) -> str:
    schema_string = json.dumps(output_schema, indent=2, ensure_ascii=False)
    return f"""You are a structured data extraction engine. Your only job is to read the provided document and return a single JSON object that strictly conforms to the schema below.

SCHEMA:
{schema_string}

STRICT RULES — follow every one of them without exception:

1. OUTPUT FORMAT
   - Return ONLY a raw JSON object. No markdown, no code fences, no prose, no explanation.
   - The root of your response must be a JSON object ({{...}}), never an array or a primitive.

2. FIELD NAMES ARE IMMUTABLE
   - Every key in your output must match the schema exactly, character by character.
   - If the schema defines "item", your output must use "item" — never "producto", "product", "element", or any other variant.
   - Do not translate, rename, abbreviate, or reformat any key.

3. NO EXTRA FIELDS
   - Your output must contain ONLY the keys defined in the schema.
   - If the document contains information that does not correspond to any schema field, discard it silently.
   - Never invent a new key because the document contains a value that seems useful but has no matching field.
   - This rule is absolute: one extra key is a critical failure.

4. MISSING INFORMATION — NO HALLUCINATION
   - If a field's value cannot be found or clearly inferred from the document, set it to null.
   - Never invent, guess, or infer a value that is not explicitly present in the document.
   - A null is always correct. A fabricated value is always wrong.

5. LISTS AND NESTED OBJECTS
   - If a schema field is an array and no items are found, return an empty array [].
   - If a schema field is an object and none of its sub-fields can be populated, return the object with all its keys set to null — do not omit the object itself.
   - For each item in an array, include only the keys defined for that item in the schema. Do not add undocumented sub-fields to array items.

6. SCHEMA FORMAT TOLERANCE
   - The schema may be a formal JSON Schema (with "type", "properties", etc.) or a plain example object showing the expected structure.
   - In both cases, extract the field names and their expected types from the schema and apply rules 2-5 accordingly.
   - If the schema uses JSON Schema format, ignore meta-keys like "$schema", "required", "description", "title" — they are not output fields.

7. BLANK OR UNREADABLE DOCUMENTS
   - If the document is blank, unreadable, or contains no extractable information, return the schema structure with every field set to null or [] as appropriate.
   - Never return an empty string or an empty object {{}} unless the schema itself is empty.
"""


async def extract_info_with_openai_vision(file_path: Path, output_schema: dict) -> Tuple[dict, Usage]:
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado para OpenAI Vision: {file_path}")

    messages_content = [{"type": "text", "text": "Extract all information from this document following the schema and rules in the system prompt."}]
    
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
    
    system_prompt = _build_system_prompt(output_schema)

    try:
        logger.info("--- INICIO DEBUG: OpenAI Vision Request ---")
        logger.info(f"Modelo: gpt-5-nano")
        logger.info(f"System Prompt: {system_prompt}")
        logger.info(f"Número de imágenes enviadas: {len(messages_content) - 1}")

        response = await openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": messages_content},
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=20000,
        )

        logger.info("--- INICIO DEBUG: OpenAI Vision Response ---")
        logger.info(response.model_dump_json(indent=2))
        logger.info("--- FIN DEBUG: OpenAI Vision Response ---")
        
        json_text = response.choices[0].message.content.strip()
        if not json_text:
            raise OpenAIError("La API de OpenAI devolvió una respuesta vacía.")

        usage = Usage.model_validate(response.usage.model_dump())
        return json.loads(json_text), usage

    except Exception as e:
        logger.exception(f"Error al procesar el CV con OpenAI Vision: {e}")
        raise OpenAIError("Error en la llamada a la API de OpenAI Vision.")


async def extract_info_from_text_with_openai(text: str, output_schema: dict) -> Tuple[dict, Usage]:
    if not text:
        raise ValueError("El texto de entrada no puede estar vacío.")

    system_prompt = _build_system_prompt(output_schema)
    user_prompt = f"Extract all information from the following text:\n\n---\n{text}\n---"

    try:
        # logger.info("--- INICIO DEBUG: OpenAI Text Request ---")
        # logger.info(f"Modelo: gpt-5-nano")
        # logger.info(f"System Prompt: {system_prompt}")
        # logger.info(f"Longitud del User Prompt: {len(user_prompt)}")

        response = await openai_client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        logger.info("--- INICIO DEBUG: OpenAI Text Response ---")
        logger.info(response.model_dump_json(indent=2))
        logger.info("--- FIN DEBUG: OpenAI Text Response ---")
        
        json_text = response.choices[0].message.content.strip()
        if not json_text:
            raise OpenAIError("La API de OpenAI (texto) devolvió una respuesta vacía.")

        usage = Usage.model_validate(response.usage.model_dump())
        return json.loads(json_text), usage

    except Exception as e:
        logger.exception(f"Error en la API de OpenAI (texto): {e}")
        raise OpenAIError("Error en la llamada a la API de OpenAI (texto).")