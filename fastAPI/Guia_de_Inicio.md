# Guía de Inicio Rápido para fastAPI-cv

Esta guía te proporcionará los pasos necesarios para arrancar la API localmente y probar su funcionalidad.

## 1. Prerrequisitos

Antes de comenzar, asegúrate de tener instalados los siguientes elementos:

*   **Python 3.8+**: Puedes descargarlo desde [python.org](https://www.python.org/).
*   **Tesseract OCR Engine** (solo si planeas procesar CVs en formato de imagen):
    *   **En Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`
    *   **En macOS (con Homebrew)**: `brew install tesseract`
    *   **En Windows**: Descarga un instalador desde [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
    *   Una vez instalado Tesseract, si no está en tu PATH, puede que necesites configurar la variable `pytesseract.pytesseract.tesseract_cmd` en `main.py` (ver `fastAPI/Code_Analysis.md`).

## 2. Configuración del Entorno Virtual

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

1.  **Navega a la raíz del proyecto**:
    ```bash
    cd /home/triskis/Escritorio/programando/AprenderPython/fastAPI-cv
    ```

2.  **Crea el entorno virtual** (si aún no lo has hecho):
    ```bash
    python3 -m venv venv
    ```

3.  **Activa el entorno virtual**:
    *   **En Linux o macOS**:
        ```bash
        source venv/bin/activate
        ```
    *   **En Windows (Command Prompt)**:
        ```cmd
        venv\Scripts\activate.bat
        ```
    *   **En Windows (PowerShell)**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   Para una activación automática al navegar al directorio, consulta `fastAPI/venv_activation.md`.

## 3. Instalación de Dependencias

Con el entorno virtual activado, instala todas las librerías necesarias:

```bash
./venv/bin/pip install -r requirements.txt
```
*(Nota: Si ya tienes el venv activado y el pip de tu venv en tu PATH, `pip install -r requirements.txt` también funcionará)*

## 4. Arrancar la API

Una vez instaladas las dependencias, puedes iniciar la aplicación FastAPI:

```bash
uvicorn main:app --reload
```

*   `main`: Se refiere al archivo `main.py`.
*   `app`: Se refiere al objeto `FastAPI()` creado dentro de `main.py`.
*   `--reload`: Reinicia el servidor automáticamente cada vez que detecta cambios en el código.

Verás un mensaje en tu terminal indicando que la API está corriendo, generalmente en `http://127.0.0.1:8000`.

## 5. Probar la API usando Swagger UI

FastAPI genera automáticamente una interfaz de usuario interactiva para la documentación de la API (Swagger UI), lo que facilita probar tus endpoints directamente desde el navegador.

1.  **Asegúrate de que la API esté corriendo** (ver paso 4). Si no lo está, iníciala con `uvicorn main:app --reload`.

2.  **Abre tu navegador** y ve a `http://127.0.0.1:8000/docs`.

3.  **Explorando la Interfaz de Swagger UI:**
    *   Verás una lista de tus endpoints API, categorizados por los métodos HTTP (GET, POST, etc.).
    *   Cada endpoint se puede expandir para mostrar más detalles, incluyendo la descripción, los parámetros esperados y los modelos de respuesta.

4.  **Probando el endpoint de saludo (`GET /`):**
    *   Busca el endpoint `GET /` (generalmente en la parte superior).
    *   Haz clic en él para expandirlo.
    *   Haz clic en el botón **"Try it out"**. Esto habilitará la sección de "Parameters".
    *   Ahora, haz clic en el botón **"Execute"**.
    *   **Resultado esperado**: En la sección "Responses", deberías ver un "Code 200" (OK) y en "Response body" una respuesta JSON como `{"message": "Hello World, from fastAPI-cv!"}`. Esto confirma que tu API está funcionando.

5.  **Probando el endpoint de subida de CV (`POST /cv`):**
    *   Busca el endpoint `POST /cv`.
    *   Haz clic en él para expandirlo.
    *   Haz clic en el botón **"Try it out"**. Esto habilitará la sección de "Parameters".
    *   Verás un campo para `file` (tipo `file`). Haz clic en **"Choose File"** y selecciona un archivo de CV desde tu ordenador. Puedes probar con archivos en formato **PDF, DOCX o una imagen** (JPG, PNG, etc.).
        *   **Importante**: Si pruebas con un archivo de imagen, asegúrate de tener el motor Tesseract OCR instalado en tu sistema, como se menciona en los prerrequisitos.
    *   Una vez seleccionado el archivo, haz clic en el botón **"Execute"**.
    *   **Resultado esperado**:
        *   En la sección "Responses", deberías ver un "Code 200" (OK).
        *   En "Response body", verás un JSON con la información extraída del CV, que incluirá:
            *   `name`: El nombre detectado (si se encuentra).
            *   `email`: El correo electrónico detectado (si se encuentra).
            *   `phone`: El número de teléfono detectado (si se encuentra).
            *   `full_text`: El texto completo extraído del CV.
        *   Si el tipo de archivo no es soportado o hay un error, recibirás un mensaje de error apropiado.
        *   Si el procesamiento es exitoso pero no se extrae información específica (como el nombre), esos campos aparecerán como `null`.

Esta interfaz te permite interactuar y depurar tu API de manera muy eficiente.

## 6. Desactivar el Entorno Virtual

Cuando hayas terminado de trabajar, puedes desactivar el entorno virtual ejecutando:

```bash
deactivate
```

---
Para un análisis más profundo del código, las librerías utilizadas y las decisiones de diseño, consulta `fastAPI/Code_Analysis.md`.
Para información detallada sobre la activación del entorno virtual, incluyendo la configuración de activación automática, consulta `fastAPI/venv_activation.md`.
