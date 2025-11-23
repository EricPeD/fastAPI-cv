# fastAPI-cv: Extractor de Información de CVs

`fastAPI-cv` es una API RESTful construida con Python y FastAPI, diseñada para procesar archivos de Currículum Vitae (CV) y extraer información clave de ellos. La API soporta múltiples formatos de archivo y devuelve los datos extraídos en un formato JSON estructurado.

Este proyecto sirve como una herramienta base para automatizar el procesamiento inicial de CVs.

## Características Principales

*   **Endpoint de Subida de Archivos**: Un endpoint `POST /cv` que acepta archivos de CV.
*   **Soporte Multi-formato**: Capacidad para procesar los formatos más comunes:
    *   `PDF (.pdf)`
    *   `Microsoft Word (.docx)`
    *   `Imágenes (.png, .jpg, etc.)` - Utiliza Tesseract para OCR.
*   **Extracción de Información Básica**: Extrae datos como email y número de teléfono utilizando expresiones regulares.
*   **Respuesta Estructurada**: Devuelve la información en un formato JSON limpio y predecible gracias a los modelos de Pydantic.
*   **Documentación Automática**: Interfaz de Swagger UI disponible en `/docs` para probar la API de forma interactiva.

## Pila Tecnológica

*   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
*   **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
*   **Procesamiento de PDF**: [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
*   **Procesamiento de DOCX**: [python-docx](https://python-docx.readthedocs.io/en/latest/)
*   **Procesamiento de Imágenes (OCR)**: [Pillow](https://python-pillow.org/) y [Pytesseract](https://pypi.org/project/pytesseract/)
*   **Validación de Datos**: [Pydantic](https://docs.pydantic.dev/)

---

## Guía de Inicio

### 1. Prerrequisitos

*   **Python 3.8+**
*   **Tesseract OCR Engine**: Necesario para procesar CVs en formato de imagen.
    *   **Ubuntu/Debian**: `sudo apt update && sudo apt install tesseract-ocr`
    *   **macOS (Homebrew)**: `brew install tesseract`
    *   **Windows**: Descargar desde [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).

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
    # En Windows usa `venv\Scripts\activate.bat`
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Ejecución

1.  **Inicia la API:**
    ```bash
    uvicorn main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000`.

2.  **Prueba la API:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/docs` para acceder a la interfaz de Swagger UI. Desde allí, puedes probar el endpoint `POST /cv` subiendo un archivo de CV.

---

## Roadmap del Proyecto

# Roadmap del Proyecto fastAPI-cv

Este documento describe el plan de desarrollo y los objetivos para el proyecto `fastAPI-cv`.

## Fase 1: MVP y Estructura Base (Completada)

*   **Objetivo Cumplido**: Se estableció el entorno de desarrollo, se creó la estructura básica de la API y se implementó un flujo funcional de subida, procesamiento y extracción básica de archivos PDF, DOCX e imágenes. Se organizó la documentación del proyecto.
*   **Tareas Realizadas**:
    *   [X] Configurar el proyecto FastAPI (`main.py`, `requirements.txt`).
    *   [X] Implementar endpoint `POST /cv` para subida de archivos.
    *   [X] Añadir lógica para procesar PDF, DOCX e Imágenes (OCR).
    *   [X] Implementar extracción básica de email y teléfono con expresiones regulares.
    *   [X] Estructurar la salida en un modelo Pydantic.
    *   [X] Realizar pruebas iniciales manuales y documentar los resultados.
    *   [X] Reorganizar y consolidar toda la documentación del proyecto.

## Fase 2: Mejora de la Extracción de Datos (Fase Actual)

*   **Objetivo**: Aumentar la cantidad y la precisión de la información extraída de los CVs, abordando los puntos débiles identificados en el MVP.
*   **Tareas Prioritarias**:
    *   [ ] **Implementar Extracción de Nombre:** Desarrollar una heurística o lógica más robusta para identificar y extraer de forma fiable el nombre del candidato.
    *   [ ] **Mejorar Robustez de Regex**: Ajustar las expresiones regulares para `phone` y `email` para que sean más tolerantes a errores de OCR y formatos variados.
    *   [ ] **Mejorar Precisión de OCR:** Añadir configuración de idioma (`lang='spa'`) a `pytesseract` para mejorar el reconocimiento en CVs en español.
    *   [ ] **Identificar Secciones del CV:** Desarrollar una lógica para identificar y aislar secciones clave como "Experiencia Laboral", "Educación" y "Habilidades".
    *   [ ] **Extracción de Habilidades (Skills)**: Una vez identificada la sección, implementar una función para extraer la lista de habilidades.

## Fase 3: Pruebas y Robustez (Próximos Pasos)

*   **Objetivo**: Crear un sistema de pruebas automatizadas que garantice la fiabilidad del código y prevenga regresiones.
*   **Tareas**:
    *   [ ] **Configurar Pytest**: Integrar el framework `pytest` en el proyecto.
    *   [ ] **Crear Tests Unitarios para Extractores**: Escribir pruebas específicas para las funciones `extract_text_from_*` y `extract_info_from_text` usando los CVs de muestra.
    *   [ ] **Crear Tests de Integración para Endpoints**: Escribir pruebas que simulen la subida de archivos al endpoint `/cv` y verifiquen que la respuesta JSON sea la esperada.
    *   [ ] **Añadir Manejo de Errores Específicos**: Refinar el manejo de excepciones para dar mensajes de error más útiles (ej. PDF corrupto, imagen de muy baja calidad, etc.).

## Fase 4: Despliegue y Mantenimiento (Futuro)

*   **Objetivo**: Preparar la API para un entorno de producción.
*   **Tareas**:
    *   [ ] Contenerización (Docker).
    *   [ ] Configuración de CI/CD (ej. GitHub Actions).
    *   [ ] Implementar un sistema de logging robusto (en lugar de `print`).
