# fastAPI-cv: Asynchronous CV Processing API with AI

`fastAPI-cv` is a high-performance, asynchronous API built with Python and FastAPI. It leverages an AI model (OpenAI's GPT) to intelligently extract structured information from multiple CV file formats (`.pdf`, `.docx`, `.png`, `.jpg`).

The API is designed for modern development workflows, featuring a webhook-based system. Instead of waiting for processing, you submit a CV and receive an immediate acknowledgment. The heavy lifting is done in the background, and the final JSON result is sent to your specified callback URL.

## Arquitectura Asíncrona

The core of this project is its non-blocking architecture:
1.  **Authentication**: A client makes a request to a user-specific endpoint (`/cv/{endpoint_id}`), authenticating with a `Bearer` token.
2.  **Immediate Response**: The API validates the request, saves the file, and immediately responds with a `202 Accepted` status and a `request_id`.
3.  **Background Processing**: A background task is created to handle the CV processing:
    *   **Text Extraction**: Extracts raw text from the file (using OCR for images).
    *   **AI Analysis**: Sends the text to an OpenAI model (gpt-4o-mini) to extract information like name, contact info, experience, and skills, based on a structured Pydantic model.
    *   **Database Logging**: The entire process, including the final result or any errors, is logged to a Supabase database.
4.  **Webhook Notification**: Once processing is complete (either successfully or with an error), the API sends a `POST` request with the JSON-formatted results to the callback URL associated with the `endpoint_id`.

This design ensures that the client application remains responsive and is ideal for integrating into larger, event-driven systems.

## Tech-Stack

*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
*   **AI-Powered Extraction**: [OpenAI GPT-4o-mini](https://openai.com/)
*   **Database**: [Supabase](https://supabase.io/) (PostgreSQL)
*   **Asynchronous HTTP Client**: [HTTPX](https://www.python-httpx.org/) (for sending webhooks)
*   **Data Validation**: [Pydantic](https://docs.pydantic.dev/)
*   **File Processing**:
    *   PDF: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
    *   DOCX: [python-docx](https://python-docx.readthedocs.io/en/latest/)
    *   Imágenes (OCR): [Pillow](https://python-pillow.org/) & [Pytesseract](https://pypi.org/project/pytesseract/)

---

## Guía de Inicio

### 1. Prerrequisitos

*   **Python 3.9+**
*   **Tesseract OCR Engine**: Required for processing CVs in image formats.
    *   **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`
    *   **macOS (Homebrew)**: `brew install tesseract`
    *   **Windows**: Download from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
*   **Supabase Project**: A configured Supabase project with the required database schema (see `fastAPI-Apuntes/4_Data_Model_and_Auth.md`).
*   **OpenAI API Key**: An API key from OpenAI.

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

### 3. Ejecución

1.  **Inicia la API:**
    ```bash
    uvicorn main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000`.

2.  **Prueba la API:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para acceder a la interfaz de Swagger UI. Desde allí, puedes probar los endpoints. Recuerda que para el endpoint de subida de CVs, necesitarás una API Key y un Endpoint ID válidos, que se gestionan a través de tu instancia de Supabase.