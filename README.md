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

# Uso de la API para Consumidores

Esta sección detalla cómo interactuar con la API `fastAPI-cv` para integrar sus funcionalidades en tus aplicaciones.

## Autenticación

Todas las peticiones a la API deben estar autenticadas. Para ello, necesitas una **API Key** válida que debes incluir en el encabezado `Authorization` de cada petición.

El formato del encabezado de autorización debe ser `Bearer TU_API_KEY`.

**Ejemplo de encabezado:**
```
Authorization: Bearer 4a868774-7654-4106-b1b6-97e05d5c09be
```

## Flujo de Uso Detallado

El proceso para procesar un CV consta de dos pasos asíncronos:
1.  **Envío del CV**: Realizas una petición `POST` con el archivo del CV. La API te confirmará la recepción inmediatamente.
2.  **Recepción de Resultados (Webhook)**: Una vez finalizado el procesamiento, la API te enviará los datos extraídos a una URL de webhook previamente configurada por ti.

### 1. Envío del CV

Para iniciar el procesamiento, envía el archivo del CV al siguiente endpoint:

`POST /cv/{endpoint_id}`

#### Parámetros de Ruta

*   `endpoint_id` (string, **requerido**): El UUID único que identifica tu endpoint configurado. La API usará este ID para saber a qué URL de webhook debe enviar los resultados del procesamiento.

#### Encabezados (Headers) Requeridos

*   `Authorization` (string): Tu clave de API con el prefijo `Bearer `.
*   `accept: application/json` (string): Indica que esperas una respuesta JSON.

#### Cuerpo de la Petición (Body)

La petición debe ser de tipo `multipart/form-data` y contener un único campo:

*   `file` (file, **requerido**): El archivo del CV que deseas procesar. Formatos soportados: PDF, DOCX, PNG, JPG.

#### Respuesta Exitosa al Envío (Código `202 Accepted`)

Si la petición es aceptada y el CV se pone en cola para procesamiento, la API responderá inmediatamente con un código `202 Accepted`.

**Cuerpo de la respuesta:**
```json
{
  "message": "CV recibido y en proceso.",
  "request_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"
}
```
*   `request_id`: Un identificador único para esta solicitud específica. Puedes usarlo para seguimiento o auditoría interna.

### 2. Recepción de Resultados (Webhook)

Una vez que el procesamiento del CV ha finalizado (ya sea con éxito o con un error), la API enviará una petición `POST` a la URL de webhook que tienes configurada para el `endpoint_id` utilizado en el envío inicial.

#### Cuerpo del Webhook (Payload JSON)

El cuerpo de la petición `POST` que recibirás en tu webhook será un JSON con la siguiente estructura:

**Ejemplo de Payload si el procesamiento fue exitoso (`status: "completed"`):**
```json
{
  "request_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "completed",
  "data": {
    "contact_info": {
      "name": "Marcelo Rodriguez",
      "email": "marcelo.rodriguez@email.com",
      "phone": "+34 123 456 789"
    },
    "summary": "Desarrollador de software con más de 5 años de experiencia en Python y desarrollo de APIs, especializado en soluciones backend escalables.",
    "experience": [
      {
        "title": "Backend Developer",
        "company": "Tech Solutions S.L.",
        "period": "Enero 2020 - Presente",
        "description": "Desarrollo y mantenimiento de microservicios con FastAPI y Django. Implementación de pipelines CI/CD con GitLab."
      }
    ],
    "education": [
      {
        "institution": "Universidad Politécnica de Madrid",
        "degree": "Grado en Ingeniería de Software",
        "period": "2015 - 2019"
      }
    ],
    "skills": ["Python", "FastAPI", "Docker", "PostgreSQL", "Git"]
  },
  "error": null
}
```

**Ejemplo de Payload si el procesamiento falló (`status: "failed"`):**
```json
{
  "request_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "failed",
  "data": null,
  "error": "No se pudo extraer el contenido del archivo. Formato no compatible o archivo corrupto."
}
```
*   `request_id`: El mismo identificador de solicitud que se te proporcionó al enviar el CV.
*   `status`: Indica el estado final del procesamiento (`completed` o `failed`).
*   `data`: Contiene el objeto JSON estructurado del CV si `status` es `completed`. Será `null` si falló.
*   `error`: Contiene un mensaje de error si `status` es `failed`. Será `null` si fue exitoso.

## Ejemplo Completo (usando cURL)

Aquí tienes un ejemplo de cómo enviar un CV usando la herramienta de línea de comandos `cURL`. Asegúrate de reemplazar los valores de marcador de posición:

```bash
curl -X 'POST' \
  'https://tu-dominio-api.com/cv/TU_ENDPOINT_ID' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer TU_API_KEY' \
  -F 'file=@/ruta/completa/a/tu/cv.pdf'
```

**Parámetros a reemplazar:**
*   `https://tu-dominio-api.com`: La URL base de tu instancia de la API (`ej. http://127.0.0.1:8000` si la corres localmente, o tu URL de `ngrok`).
*   `TU_ENDPOINT_ID`: El UUID de tu endpoint configurado (ej. `d3049ccd-ede3-40b0-a475-d8f620e4b495`).
*   `TU_API_KEY`: Tu clave de API generada (`ej. 4a868774-7654-4106-b1b6-97e05d5c09be`).
*   `/ruta/completa/a/tu/cv.pdf`: La ruta completa a tu archivo CV local.

---

# Guía de Inicio para Desarrolladores

Esta sección proporciona instrucciones para configurar y ejecutar el proyecto `fastAPI-cv` en tu entorno de desarrollo local.

### 1. Prerrequisitos

*   **Python 3.9+**
*   **Motor Tesseract OCR**: Necesario para procesar CVs en formatos de imagen.
    *   **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`
    *   **macOS (Homebrew)**: `brew install tesseract`
    *   **Windows**: Descargar e instalar desde [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Asegúrate de añadir `tesseract.exe` a tu PATH.
*   **Proyecto Supabase**: Un proyecto Supabase configurado con el esquema de base de datos requerido (consulta `fastAPI-Apuntes/4_Data_Model_and_Auth.md` para detalles del esquema).
*   **Clave API de OpenAI**: Una clave API de OpenAI activa.

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
    Crea un archivo `.env` en la raíz del proyecto y añade las siguientes claves. Puedes usar el `.env.example` como plantilla y rellenarlo con tus credenciales:
    ```env
    # .env
    OPENAI_API_KEY="sk-..."
    SUPABASE_URL="https://<your-project-ref>.supabase.co"
    SUPABASE_KEY="your-supabase-anon-key"
    ```

### 3. Preparación de la Base de Datos para Pruebas (Opcional)

Para probar la API localmente, tu base de datos de Supabase **debe contener datos de usuarios, API Keys y configuraciones de endpoints**.

*   **Usuarios**: Asegúrate de tener al menos un registro en la tabla `public.users`.
*   **API Keys**: Inserta manualmente un registro en `public.api_keys` o usa un sistema externo para generar una API Key asociada a tu usuario. **Guarda la clave completa (`ID.HASH`)**, la necesitarás para las pruebas de API.
*   **Endpoints**: Inserta al menos un registro en `public.endpoints`.
    *   Dale un `name` y asócialo a tu `id_user`.
    *   En el campo `info` (JSONB), asegúrate de tener una clave `callbackURL` válida (ej. `https://webhook.site/your-unique-url`).
    *   **Copia el `id` (UUID) de este endpoint**. Lo necesitarás para las peticiones de prueba.
*   **Scripts de Ayuda**: Para facilitar la creación de estos datos durante el desarrollo sin acceder directamente al dashboard de Supabase, puedes consultar la documentación interna en `fastAPI-Apuntes/4_Data_Model_and_Auth.md` para más detalles sobre cómo modelar los datos necesarios y cómo se generan las API keys de forma segura.

### 4. Ejecución

1.  **Inicia la API:**
    ```bash
    uvicorn src.main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000`.

2.  **Acceso a la Documentación Interactiva:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para acceder a la interfaz de Swagger UI, donde podrás explorar todos los endpoints disponibles.

---

# Hitos Recientes y Robustez del Sistema

Tras un riguroso proceso de refactorización y depuración, el sistema ha alcanzado un alto nivel de funcionalidad y fiabilidad:

*   **Resolución Completa de Errores Críticos**: Se identificaron y corrigieron múltiples `TypeError`s relacionados con la asincronía del cliente `supabase-py`, `NameError`s, problemas de formato de API Key y errores de validación Pydantic (`ValidationError`) en la integración con OpenAI.
*   **Manejo Robusto de `public.endpoints`**: Se diagnosticó y resolvió el problema de `404 Not Found` que surgía de una tabla de `endpoints` vacía, implementando un flujo para asegurar la existencia de configuraciones de endpoint.
*   **Flujo Operativo End-to-End**: La tubería completa de procesamiento de CVs funciona correctamente, desde la autenticación y validación del endpoint, hasta la extracción de texto (incluyendo OCR), la integración con OpenAI para datos estructurados, el registro en Supabase, la notificación por webhook y la limpieza de archivos temporales.
*   **Pruebas de Carga Concurrente Exitosas**: El sistema ha sido probado con éxito enviando múltiples archivos PDF concurrentemente, demostrando su capacidad para manejar cargas de trabajo asíncronas de manera eficiente.
*   **Manejo Adecuado de Errores**: Se verifica el correcto manejo de errores para archivos no soportados (ej. `.md`), actualizando el estado de la solicitud a 'failed' y enviando una notificación detallada al webhook.

El proyecto `fastAPI-cv` está ahora en un estado estable y preparado para futuras expansiones.
