# fastAPI-cv: API Asíncrona de Procesamiento de CVs con IA

`fastAPI-cv` es una API asíncrona de alto rendimiento construida con Python y FastAPI. Aprovecha un modelo de IA (GPT de OpenAI) para extraer inteligentemente información estructurada de múltiples formatos de archivo de CV (`.pdf`, `.docx`, `.png`, `.jpg`).

La API está diseñada para flujos de trabajo de desarrollo modernos, con un sistema basado en webhooks. En lugar de esperar el procesamiento, usted envía un CV y recibe un acuse de recibo inmediato. El trabajo pesado se realiza en segundo plano, y el resultado JSON final se envía a su URL de callback especificada.

## Arquitectura Asíncrona

El núcleo de este proyecto es su arquitectura no bloqueante, la cual ha sido rigurosamente depurada y confirmada como robusta bajo carga concurrente:
1.  **Autenticación**: Un cliente realiza una petición a un endpoint específico de usuario (`/cv/{endpoint_id}`), autenticándose con un token `Bearer`.
2.  **Respuesta Inmediata**: La API valida la petición, guarda el archivo y responde inmediatamente con un estado `202 Accepted` y un `request_id`.
3.  **Procesamiento en Segundo Plano**: Se crea una tarea en segundo plano para manejar el procesamiento del CV:
    *   **Extracción de Texto**: Extrae el texto sin formato del archivo (usando OCR para imágenes).
    *   **Análisis con IA**: Envía el texto a un modelo de OpenAI (gpt-4o-mini) para extraer información como nombre, datos de contacto, experiencia y habilidades, basándose en un modelo Pydantic estructurado.
    *   **Registro en Base de Datos**: Todo el proceso, incluyendo el resultado final o cualquier error, se registra en una base de datos Supabase.
4.  **Notificación por Webhook**: Una vez completado el procesamiento (ya sea con éxito o con un error), la API envía una petición `POST` con los resultados en formato JSON a la URL de callback asociada con el `endpoint_id`.

Este diseño asegura que la aplicación cliente permanezca responsiva y es ideal para la integración en sistemas más grandes y basados en eventos.

## Tech-Stack

*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
*   **Extracción Potenciada por IA**: [OpenAI GPT-4o-mini](https://openai.com/)
*   **Base de Datos**: [Supabase](https://supabase.io/) (PostgreSQL)
*   **Cliente HTTP Asíncrono**: [HTTPX](https://www.python-httpx.org/) (para enviar webhooks)
*   **Validación de Datos**: [Pydantic](https://docs.pydantic.dev/)
*   **Procesamiento de Archivos**:
    *   PDF: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
    *   DOCX: [python-docx](https://python-docx.readthedocs.io/en/latest/)
    *   Imágenes (OCR): [Pillow](https://python-pillow.org/) & [Pytesseract](https://pypi.org/project/pytesseract/)

---

## Guía de Inicio

### 1. Prerrequisitos

*   **Python 3.9+**
*   **Motor Tesseract OCR**: Necesario para procesar CVs en formatos de imagen.
    *   **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`
    *   **macOS (Homebrew)**: `brew install tesseract`
    *   **Windows**: Descargar desde [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
*   **Proyecto Supabase**: Un proyecto Supabase configurado con el esquema de base de datos requerido (ver `fastAPI-Apuntes/4_Data_Model_and_Auth.md`).
*   **Clave API de OpenAI**: Una clave API de OpenAI.

### 2. Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/EricPeD/fastAPI-cv.git
    cd fastAPI-cv
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # En Windows, usa: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto y añade las siguientes claves. Puedes usar el `.env.example` como plantilla:
    ```env
    # .env
    OPENAI_API_KEY="sk-..."
    SUPABASE_URL="https://<your-project-ref>.supabase.co"
    SUPABASE_KEY="your-supabase-anon-key"
    ```

### 3. Preparación de la Base de Datos para Pruebas (Opcional para Desarrollo)

Para probar la API localmente, tu base de datos de Supabase **debe contener datos de usuarios, API Keys y configuraciones de endpoints**.

*   **Usuarios**: Asegúrate de tener un registro en la tabla `public.users`.
*   **API Keys**: Inserta manualmente un registro en `public.api_keys` o usa un sistema externo para generar una API Key asociada a tu usuario. **Guarda la clave completa (`ID.HASH`)**, la necesitarás para las pruebas.
*   **Endpoints**: Inserta un registro en `public.endpoints`.
    *   Dale un `name` y asócialo a tu `id_user`.
    *   En el campo `info` (JSONB), asegúrate de tener una clave `callbackURL` (ej. `https://webhook.site/your-unique-url`).
    *   **Copia el `id` (UUID) de este endpoint**. Lo necesitarás para la URL de la petición.
*   **Scripts de Ayuda**: Para facilitar la creación de estos datos durante el desarrollo sin acceder directamente al dashboard de Supabase, puedes crear un endpoint temporal en tu aplicación FastAPI (consulta `fastAPI-Apuntes/9_Full_Debugging_Log.md` para ejemplos de cómo se hizo durante la depuración).

### 4. Ejecución

1.  **Inicia la API:**
    ```bash
    uvicorn src.main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000`.

2.  **Prueba la API:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para acceder a la interfaz de Swagger UI. Desde allí, puedes probar los endpoints. Recuerda que para el endpoint de subida de CVs (`POST /cv/{endpoint_id}`), necesitarás una API Key y un Endpoint ID válidos, que deben estar configurados previamente en tu instancia de Supabase.

### 5. Hitos Recientes y Robustez del Sistema

Tras un riguroso proceso de refactorización y depuración, el sistema ha alcanzado un alto nivel de funcionalidad y fiabilidad:

*   **Resolución Completa de Errores Críticos**: Se identificaron y corrigieron múltiples `TypeError`s relacionados con la asincronía del cliente `supabase-py`, `NameError`s, problemas de formato de API Key y errores de validación Pydantic (`ValidationError`) en la integración con OpenAI.
*   **Manejo Robusto de `public.endpoints`**: Se diagnosticó y resolvió el problema de `404 Not Found` que surgía de una tabla de `endpoints` vacía, implementando un flujo para asegurar la existencia de configuraciones de endpoint.
*   **Flujo Operativo End-to-End**: La tubería completa de procesamiento de CVs funciona correctamente, desde la autenticación y validación del endpoint, hasta la extracción de texto (incluyendo OCR), la integración con OpenAI para datos estructurados, el registro en Supabase, la notificación por webhook y la limpieza de archivos temporales.
*   **Pruebas de Carga Concurrente Exitosas**: El sistema ha sido probado con éxito enviando múltiples archivos PDF concurrentemente, demostrando su capacidad para manejar cargas de trabajo asíncronas de manera eficiente.
*   **Manejo Adecuado de Errores**: Se verifica el correcto manejo de errores para archivos no soportados (ej. `.md`), actualizando el estado de la solicitud a 'failed' y enviando una notificación detallada al webhook.

El proyecto `fastAPI-cv` está ahora en un estado estable y preparado para futuras expansiones.