import asyncio
import httpx
import os
from pathlib import Path

# --- Configuración ---
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT_ID = (
    "1edb42d6-2410-4e52-92a1-61ac958182a4"  # Reemplaza con tu ID de endpoint real
)
API_KEY = "082db487-cc96-4312-beed-ece21d33bc5d.e5556906dacd08893ebbfbf5864f2a91801130497387a7a0cdb6e52b4b4822d0"  # Reemplaza con tu API Key real (ej. "082db487-...d.e5556906...")
FILES_TO_SEND = [
    # Path("testCV/cv/sample_cv.pdf"),
    # Path("testCV/cv/sample_cv_variant_01.pdf"),
    # Path("testCV/cv/sample_cv_variant_02.pdf"),
    # Path("testCV/cv/sample_cv_variant_03.pdf"),
    # Path("testCV/cv/sample_cv_variant_04.pdf"),
    # Path("testCV/cv/sample_cv_variant_05.pdf"),
    # Path("testCV/cv/sample_cv_variant_06.pdf"),
    # Path("testCV/cv/sample_cv_variant_07.pdf"),
    # Path("testCV/cv/sample_cv_variant_08.pdf"),
    # Path("testCV/cv/sample_cv_variant_09.pdf"),
    # Path("testCV/cv/sample_cv_variant_10.pdf"),
    # Path("testCV/cv/sample_cv_variant_11.pdf"),
    # Path("testCV/cv/sample_cv_variant_12.pdf"),
    # Path("testCV/cv/sample_cv_variant_13.pdf"),
    # Path("testCV/cv/sample_cv_variant_14.pdf"),
    Path("testCV/cv/CV_Nicolas_Penuela.png"),
    Path("testCV/cv/CV_Nicolas_Penuela.png"),
    Path("testCV/cv/CV_Nicolas_Penuela.png"),
    Path("testCV/cv/CV_Nicolas_Penuela.png"),
]


async def send_file_request(
    client: httpx.AsyncClient, file_path: Path, request_num: int
):
    url = f"{BASE_URL}/cv/{ENDPOINT_ID}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        # Abrir el archivo en modo binario
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}
            print(f"[{request_num}] Enviando {file_path.name} a {url}...")
            response = await client.post(
                url, headers=headers, files=files, timeout=60.0
            )
            response.raise_for_status()  # Lanza excepción para códigos de estado 4xx/5xx
            print(
                f"[{request_num}] Respuesta para {file_path.name}: {response.status_code} - {response.json()}"
            )
            return response.json()
    except httpx.RequestError as e:
        print(f"[{request_num}] Error de petición para {file_path.name}: {e}")
    except httpx.HTTPStatusError as e:
        print(
            f"[{request_num}] Error HTTP para {file_path.name}: {e.response.status_code} - {e.response.text}"
        )
    except Exception as e:
        print(f"[{request_num}] Error inesperado para {file_path.name}: {e}")
    return None


async def main():
    async with httpx.AsyncClient() as client:
        tasks = []
        for i, file_path in enumerate(FILES_TO_SEND):
            if file_path.exists():
                tasks.append(send_file_request(client, file_path, i + 1))
            else:
                print(f"[!] Advertencia: Archivo no encontrado: {file_path}. Saltando.")

        print(f"Enviando {len(tasks)} solicitudes concurrentemente...")
        results = await asyncio.gather(*tasks)
        print("\n--- Resultados de todas las solicitudes ---")
        for i, result in enumerate(results):
            if result:
                print(
                    f"Solicitud {i + 1} ({FILES_TO_SEND[i].name}): Éxito. Request ID: {result.get('request_id')}"
                )
            else:
                print(f"Solicitud {i + 1} ({FILES_TO_SEND[i].name}): Fallida.")


if __name__ == "__main__":
    asyncio.run(main())
