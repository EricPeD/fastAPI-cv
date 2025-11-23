# Roadmap del Proyecto fastAPI-cv

Este documento describe el plan de desarrollo y los objetivos para el proyecto fastAPI-cv, organizados por fases.
## Fase 1: Configuración Inicial y API Básica (MVP)

*   **Objetivo**: Establecer el entorno de desarrollo, crear la estructura básica de la API y un endpoint funcional de prueba.
*   **Tareas**:
    *   [X] Crear `GEMINI.md` para el contexto del proyecto.
    *   [X] Crear `fastAPI/Roadmap.md` (este archivo).
    *   [X] Configurar la estructura inicial del proyecto FastAPI (`main.py`, `requirements.txt`).
    *   [X] Implementar un "Hello World" en FastAPI.
    *   [ ] Realizar el primer commit del proyecto.

## Fase 2: Recepción y Pre-procesamiento de CVs

*   **Objetivo**: Permitir la subida de archivos de CV a través de un endpoint y preparar su contenido para el análisis.
*   **Tareas**:
    *   [X] Implementar el endpoint para la subida de archivos CV (Word, PDF, imágenes).
    *   [X] Desarrollar un sistema de detección del tipo de archivo (MIME type).
    *   [X] Guardar temporalmente los archivos subidos.

## Fase 3: Procesamiento de Contenido

*   **Objetivo**: Extraer texto de los diferentes formatos de CV.
*   **Tareas**:
    *   [X] Añadir la lógica para procesar archivos PDF (usando librerías como `PyMuPDF` o `pdfplumber`).
    *   [X] Añadir la lógica para procesar archivos DOCX (usando `python-docx`).
    *   [X] Añadir la lógica para procesar archivos de imagen (OCR usando `pytesseract`).
    *   [X] Consolidar el texto extraído en un formato unificado.

## Fase 4: Extracción y Estructuración de Información

*   **Objetivo**: Analizar el texto del CV para identificar y extraer información clave, estructurándola en formato JSON.
*   **Tareas**:
    *   [X] Implementar funciones de extracción de información (ej. expresiones regulares para emails, teléfonos).
    *   [ ] Identificar secciones comunes de CV (experiencia, educación, habilidades).
    *   [X] Estructurar la información extraída en un modelo Pydantic para el JSON de salida.
    *   [ ] Manejar casos donde la información no es fácilmente identificable.

## Fase 5: Pruebas y Refinamiento

*   **Objetivo**: Asegurar la robustez y precisión del sistema.
*   **Tareas**:
    *   [ ] Escribir tests unitarios para cada componente (endpoints, procesadores de archivos, extractores de información).
    *   [ ] Escribir tests de integración para el flujo completo.
    *   [ ] Optimizar el rendimiento del procesamiento.
    *   [ ] Mejorar la calidad de la extracción de datos.

## Fase 6: Despliegue y Mantenimiento (Futuro)

*   **Objetivo**: Preparar la API para un entorno de producción.
*   **Tareas**:
    *   [ ] Contenerización (Docker).
    *   [ ] Configuración de CI/CD.
    *   [ ] Monitoreo y logging.
    *   [ ] Documentación de la API (OpenAPI/Swagger UI ya incluido en FastAPI).
    *   [ ] Mejoras continuas en los algoritmos de extracción.
