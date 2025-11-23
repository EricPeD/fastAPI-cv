# Análisis Detallado del Código: `main.py`

Este documento proporciona un análisis exhaustivo del archivo `main.py`, desglosando cada sección, explicando su propósito, las decisiones de diseño, las librerías utilizadas (incluyendo pros y contras), y posibles mejoras.

## 1. Importaciones

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import os
import shutil
import mimetypes
import fitz # PyMuPDF
from docx import Document # python-docx
from PIL import Image # Pillow
import pytesseract
from pydantic import BaseModel
import re
```

### Propósito
Esta sección importa todas las clases, funciones y módulos necesarios para la funcionalidad de la API.

### Librerías Utilizadas y Razón de Elección

*   **`fastapi`**:
    *   **Propósito**: Framework web para construir APIs con Python, conocido por su alto rendimiento (gracias a Starlette y Pydantic) y su facilidad de uso, especialmente con tipado de datos.
    *   **Pros**:
        *   **Rendimiento**: Muy rápido, a la par de Node.js y Go (gracias a Uvicorn).
        *   **Productividad**: Tipado estático con Pydantic y Python 3.6+ permite autocompletado, validación de datos y manejo de errores automático.
        *   **Documentación Automática**: Genera automáticamente documentación interactiva (Swagger UI y ReDoc) de la API.
        *   **Moderno**: Soporte para programación asíncrona (`async`/`await`).
    *   **Contras**:
        *   **Curva de Aprendizaje**: Puede ser un poco más pronunciado para quienes no están familiarizados con el tipado de Python y la programación asíncrona.
        *   **Menos Madurez** (comparado con Django/Flask): Aunque está creciendo rápidamente, tiene menos ecosistema y plugins que frameworks más antiguos.

*   **`pathlib.Path`**:
    *   **Propósito**: Ofrece una forma orientada a objetos de manejar rutas de sistemas de archivos.
    *   **Pros**:
        *   **Legibilidad**: Código más limpio y legible al manipular rutas.
        *   **Compatibilidad**: Maneja la diferencia entre sistemas operativos (Windows vs. Unix) de manera transparente.
        *   **Funcionalidad**: Métodos útiles para crear, borrar, unir, verificar existencias, etc., de rutas.
    *   **Contras**:
        *   **No Universalmente Adoptado**: Algunas librerías antiguas aún esperan strings para las rutas.

*   **`os`**:
    *   **Propósito**: Interacción con el sistema operativo, principalmente para operaciones de archivos y directorios de bajo nivel (aunque `pathlib` cubre muchas de sus funciones). Se usa aquí para `os.remove()`.
    *   **Pros**:
        *   **Estándar**: Parte de la biblioteca estándar de Python.
        *   **Control Fino**: Permite operaciones directas con el sistema de archivos.
    *   **Contras**:
        *   **Menos Legible**: Las operaciones de ruta son menos intuitivas que con `pathlib`.
        *   **Potencial de Errores**: Más propenso a errores de ruta si no se maneja cuidadosamente la compatibilidad del sistema operativo.

*   **`shutil`**:
    *   **Propósito**: Operaciones de alto nivel sobre archivos y colecciones de archivos, como copiar archivos (`shutil.copyfileobj`).
    *   **Pros**:
        *   **Eficiente**: Ideal para copiar grandes archivos en trozos (chunks) sin cargarlos completamente en memoria.
        *   **Facilidad de Uso**: Simplifica tareas comunes de manejo de archivos.
    *   **Contras**:
        *   **No Hay Muchos Contras**: Es una librería robusta y estándar para su propósito.

*   **`mimetypes`**:
    *   **Propósito**: Determinar el tipo MIME de un archivo a partir de su nombre o extensión.
    *   **Pros**:
        *   **Estándar**: Biblioteca estándar de Python.
        *   **Utilidad**: Esencial para la validación de archivos basada en su tipo.
    *   **Contras**:
        *   **Limitaciones**: La detección se basa principalmente en la extensión del archivo, no en su contenido real, lo que puede ser engañoso o insuficiente para archivos malformados o con extensiones incorrectas. Puede fallar en detectar tipos raros.

*   **`fitz` (PyMuPDF)**:
    *   **Propósito**: Para la extracción de texto de archivos PDF. PyMuPDF es un binding de Python para MuPDF, un visor y renderizador de PDF, XPS y e-book muy eficiente.
    *   **Pros**:
        *   **Rendimiento**: Extremadamente rápido y eficiente para procesar PDFs grandes.
        *   **Capacidades**: Permite extraer texto, imágenes, metadatos, renderizar páginas a imágenes, etc.
        *   **Fiabilidad**: Muy robusto para diferentes estructuras de PDF.
    *   **Contras**:
        *   **Instalación**: Puede tener dependencias de compilación en algunos sistemas, aunque los wheels precompilados simplifican esto.
        *   **Licencia**: Es de uso comercial gratuito, pero puede requerir atención a la licencia para proyectos específicos.

*   **`docx` (python-docx)**:
    *   **Propósito**: Para leer, escribir y modificar archivos `.docx` (Microsoft Word 2007+).
    *   **Pros**:
        *   **Facilidad de Uso**: API intuitiva para trabajar con documentos Word.
        *   **Extracción de Texto**: Permite acceder al texto de párrafos y tablas fácilmente.
    *   **Contras**:
        *   **Solo .docx**: No soporta formatos más antiguos como `.doc`.
        *   **Limitaciones**: No está diseñado para un renderizado exacto o para manejar todas las complejidades de formato de Word (como extraer contenido de cuadros de texto flotantes sin una iteración más profunda).

*   **`PIL.Image` (Pillow)**:
    *   **Propósito**: Biblioteca de procesamiento de imágenes para Python. Usada aquí para abrir y manipular imágenes antes de pasarlas a Tesseract.
    *   **Pros**:
        *   **Estándar de facto**: Ampliamente utilizada y bien mantenida.
        *   **Versatilidad**: Soporta una gran variedad de formatos de imagen y ofrece muchas operaciones de procesamiento.
    *   **Contras**:
        *   **Manejo de Memoria**: Para imágenes muy grandes, puede consumir bastante memoria.

*   **`pytesseract`**:
    *   **Propósito**: Un wrapper de Python para la biblioteca Tesseract-OCR de Google. Permite realizar reconocimiento óptico de caracteres (OCR) en imágenes.
    *   **Pros**:
        *   **Potente**: Tesseract es uno de los motores OCR de código abierto más precisos.
        *   **Facilidad de Integración**: Simple de usar una vez que Tesseract está instalado.
        *   **Soporte Multilingüe**: Soporta muchos idiomas.
    *   **Contras**:
        *   **Dependencia Externa**: Requiere que el motor Tesseract-OCR esté instalado en el sistema, lo cual es una dependencia externa no gestionada por `pip`. Esto añade un paso manual de configuración para el usuario.
        *   **Precisión**: La precisión del OCR puede variar significativamente dependiendo de la calidad de la imagen (resolución, ruido, tipo de fuente).

*   **`pydantic.BaseModel`**:
    *   **Propósito**: Creación de modelos de datos usando tipado de Python, con validación de datos en tiempo de ejecución. FastAPI lo usa extensivamente para definir esquemas de solicitud y respuesta.
    *   **Pros**:
        *   **Validación Automática**: Valida automáticamente los datos de entrada y salida de la API.
        *   **Serialización/Deserialización**: Convierte objetos Python a/desde JSON de manera eficiente.
        *   **Documentación**: Contribuye a la generación automática de esquemas OpenAPI.
        *   **Autocompletado**: Mejora la experiencia de desarrollo con el IDE.
    *   **Contras**:
        *   **Sobrecarga**: Para modelos de datos muy pequeños o simples, puede parecer una sobrecarga.

*   **`re`**:
    *   **Propósito**: Módulo de expresiones regulares de Python, utilizado para buscar patrones de texto (como emails y números de teléfono) dentro del texto extraído del CV.
    *   **Pros**:
        *   **Potente**: Extremadamente flexible para la búsqueda y manipulación de texto basada en patrones.
        *   **Estándar**: Parte de la biblioteca estándar de Python.
    *   **Contras**:
        *   **Complejidad**: Las expresiones regulares pueden ser difíciles de leer, escribir y depurar, especialmente para patrones complejos.
        *   **Limitaciones**: Para tareas NLP más avanzadas (ej. reconocimiento de entidades nombradas más allá de patrones simples), pueden no ser suficientes y requerirían librerías NLP dedicadas.

### Consideraciones Adicionales
La elección de estas librerías demuestra un buen equilibrio entre rendimiento, facilidad de uso y la capacidad de manejar los requisitos específicos de procesamiento de CVs. La principal desventaja es la dependencia externa de Tesseract para OCR, que requiere una instalación manual.

## 2. Configuración Inicial y Modelo de Datos

```python
# Configura la ruta al ejecutable de Tesseract si no está en el PATH
# Por ejemplo, en Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# En Linux, si no está en el PATH, puedes especificar la ruta completa.
# Si está en el PATH, no es necesario especificarlo.
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

app = FastAPI()

# Directorio temporal para almacenar los CVs
TEMP_CV_DIR = Path("temp")
TEMP_CV_DIR.mkdir(exist_ok=True) # Asegurarse de que el directorio exista

# Modelo Pydantic para la información extraída del CV
class CVInfo(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    # Puedes añadir más campos aquí según sea necesario (ej. experience, education, skills)
    full_text: str | None = None # El texto completo extraído del CV
```

### Propósito
Esta sección inicializa la aplicación FastAPI, configura un directorio temporal para la gestión de archivos y define el modelo de datos que se utilizará para estructurar la información extraída de los CVs.

### Razón de las Elecciones de Código

*   **Configuración de Tesseract**: La línea comentada `pytesseract.pytesseract.tesseract_cmd` es crucial para entornos donde el ejecutable de Tesseract-OCR no está en el `PATH` del sistema. Se deja comentada porque en muchos sistemas Linux modernos, Tesseract ya está en el `PATH` por defecto. Si no lo estuviera, el usuario debería descomentar y ajustar la ruta. Esta es una advertencia importante sobre una dependencia externa.
*   **`app = FastAPI()`**: Inicializa la aplicación FastAPI. Es el punto de entrada para definir rutas y la lógica de la API.
*   **`TEMP_CV_DIR = Path("temp")`**: Define una ruta al directorio temporal. Usar `pathlib.Path` aquí es una buena práctica por las razones mencionadas en la sección de importaciones.
*   **`TEMP_CV_DIR.mkdir(exist_ok=True)`**: Crea el directorio `temp` si no existe. `exist_ok=True` evita un error si el directorio ya existe, lo que es útil para reinicios de la aplicación.
*   **`class CVInfo(BaseModel):`**: Define la estructura de datos para la salida JSON.
    *   **Tipado**: `str | None` indica que los campos pueden ser una cadena de texto o `None`, lo que los hace opcionales y robustos ante la falta de información en un CV.
    *   **Flexibilidad**: Los comentarios indican dónde se podrían añadir más campos para una extracción más detallada.
    *   **`full_text`**: Incluir el texto completo extraído es útil para depuración y para futuros análisis más complejos que podrían no estar cubiertos por la extracción inicial.

### Pros y Contras de las Elecciones

*   **Tesseract Config**:
    *   **Pro**: Permite flexibilidad en la ubicación de la instalación de Tesseract.
    *   **Contra**: Requiere que el usuario sepa la ruta de su instalación de Tesseract si no está en el PATH, añadiendo un paso manual.
*   **Directorio Temporal**:
    *   **Pro**: Facilita el procesamiento de archivos por librerías que requieren rutas de archivo. Aísla los archivos de los procesos de la aplicación. `shutil.copyfileobj` es eficiente para manejar streams de archivos.
    *   **Contra**: Introduce la necesidad de gestionar la limpieza de estos archivos temporales (lo cual se hace con `os.remove()` en el endpoint). Puede ser un vector de ataque si no se sanea el nombre del archivo (se aborda con `Path(file.filename).name`).
*   **`CVInfo` Pydantic Model**:
    *   **Pros**:
        *   **Validación de Datos**: Garantiza que la salida JSON siempre siga una estructura definida.
        *   **Documentación Automática**: FastAPI usa este modelo para generar la documentación OpenAPI (Swagger UI), haciendo la API autodescriptiva.
        *   **Coherencia**: Fuerza una estructura de datos consistente.
    *   **Contras**:
        *   **Rigidez Inicial**: Si la estructura de datos necesita cambiar drásticamente, el modelo debe actualizarse.

### Posibles Mejoras
*   **Variables de Entorno**: La ruta de `tesseract_cmd` podría configurarse mediante una variable de entorno para mayor flexibilidad y no requerir modificar el código.
*   **Limpieza de Directorio**: Podríamos añadir una lógica al inicio de la aplicación para limpiar el directorio `temp` de archivos antiguos o que quedaron de ejecuciones anteriores fallidas.
*   **Modelos de Datos más Granulares**: Para campos como "experiencia" o "educación", se podrían definir modelos Pydantic anidados para una estructura más rica y validada.

## 3. Funciones Auxiliares para Extracción de Texto

Esta sección define las funciones que se encargan de la lógica de extracción de texto para cada tipo de archivo soportado.

### 3.1. `get_mime_type(file_path: Path)`

```python
def get_mime_type(file_path: Path):
    """
    Intenta obtener el tipo MIME de un archivo.
    Prioriza la detección por contenido si es posible, si no, usa la extensión.
    """
    mime_type, _ = mimetypes.guess_type(file_path.name)
    return mime_type
```

### Propósito
Detecta el tipo MIME de un archivo basándose en su extensión, lo que es crucial para redirigir el archivo al extractor de texto correcto.

### Razón de las Elecciones de Código
*   **`mimetypes.guess_type(file_path.name)`**: Utiliza el nombre del archivo para inferir su tipo MIME. Es la forma estándar de `mimetypes` para hacerlo.
*   **`file_path.name`**: Se usa `.name` de `pathlib` para obtener solo el nombre del archivo con su extensión, lo cual es lo que `mimetypes.guess_type` espera.

### Pros y Contras
*   **Pros**:
    *   **Simplicidad**: Fácil de implementar.
    *   **Estándar**: Utiliza una biblioteca estándar de Python.
    *   **Suficiente para Casos Comunes**: Funciona bien para archivos con extensiones estándar y correctas.
*   **Contras**:
    *   **Basado en Extensión**: La principal limitación es que solo adivina el tipo MIME basándose en la extensión del archivo. Un archivo `pdf` renombrado a `txt` se detectaría como `text/plain`, lo cual es incorrecto. Para una detección más robusta, se necesitaría analizar los "magic bytes" del archivo (contenido real), lo que requeriría librerías adicionales (ej. `python-magic`).
    *   **Incompleto**: Puede no detectar el tipo MIME para todas las extensiones o tipos de archivos.

### Posibles Mejoras
*   **Detección Robusta**: Implementar o integrar una detección de tipo MIME basada en "magic bytes" (ej. con `python-magic`) para una mayor fiabilidad, especialmente para la seguridad y el manejo de archivos malformados o engañosos.

### 3.2. `extract_text_from_pdf(pdf_path: Path) -> str`

```python
def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrae texto de un archivo PDF usando PyMuPDF.
    """
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        document.close()
    except Exception as e:
        print(f"Error al extraer texto de PDF {pdf_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {e}")
    return text
```

### Propósito
Encapsula la lógica para extraer todo el texto de un archivo PDF.

### Razón de las Elecciones de Código
*   **`fitz.open(pdf_path)`**: Abre el documento PDF. PyMuPDF es muy eficiente para esto.
*   **Bucle por Páginas**: Itera sobre cada página del documento.
*   **`page.get_text()`**: Extrae el texto de la página actual.
*   **`document.close()`**: Cierra el documento, liberando recursos.
*   **Manejo de Errores**: Captura excepciones durante el procesamiento del PDF y lanza una `HTTPException` para informar al cliente.

### Pros y Contras
*   **Pros**:
    *   **Eficiencia**: PyMuPDF es extremadamente rápido y consume pocos recursos.
    *   **Precisión**: Generalmente extrae el texto de PDFs de forma muy fiable.
    *   **Integración**: Fácil de usar.
*   **Contras**:
    *   **Dependencia Externa**: Requiere PyMuPDF, que es una dependencia relativamente grande.
    *   **Formato de Salida**: El texto extraído puede no mantener el formato original (espacios, saltos de línea) de manera perfecta, especialmente en PDFs complejos con múltiples columnas o diseños no estándar.

### Posibles Mejoras
*   **Opciones de Extracción**: PyMuPDF ofrece varias opciones para `get_text()` (ej. `textpage`, `html`, `xml`, `dict`). Podríamos experimentar con estas para ver si alguna mejora la calidad del texto extraído para ciertos tipos de CVs.
*   **Limpieza de Texto**: Implementar una limpieza post-extracción para eliminar encabezados/pies de página repetitivos o caracteres extraños.

### 3.3. `extract_text_from_docx(docx_path: Path) -> str`

```python
def extract_text_from_docx(docx_path: Path) -> str:
    """
    Extrae texto de un archivo DOCX usando python-docx.
    """
    text = ""
    try:
        document = Document(docx_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error al extraer texto de DOCX {docx_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el DOCX: {e}")
    return text
```

### Propósito
Encapsula la lógica para extraer todo el texto de un archivo DOCX.

### Razón de las Elecciones de Código
*   **`Document(docx_path)`**: Abre el documento DOCX.
*   **`document.paragraphs`**: Itera sobre todos los párrafos del documento. `python-docx` organiza el contenido en párrafos, que es una forma lógica de extraer texto.
*   **`paragraph.text`**: Obtiene el texto de cada párrafo.
*   **Manejo de Errores**: Captura excepciones y lanza `HTTPException`.

### Pros y Contras
*   **Pros**:
    *   **Simplicidad**: Muy fácil de usar para extraer texto.
    *   **Fiabilidad**: Funciona bien para extraer texto de la mayoría de los documentos DOCX estándar.
*   **Contras**:
    *   **Solo Párrafos**: No extrae texto de otros elementos como cuadros de texto flotantes, formas o SmartArt sin una lógica adicional más compleja.
    *   **Formato**: Puede perder el formato original (negritas, cursivas, etc.) al concatenar el texto.

### Posibles Mejoras
*   **Extraer de Tablas**: Muchos CVs usan tablas para estructurar información. Se podría añadir lógica para extraer contenido de tablas.
*   **Contenido Adicional**: Explorar la API de `python-docx` para extraer texto de otros elementos que puedan contener información relevante.

### 3.4. `extract_text_from_image(image_path: Path) -> str`

```python
def extract_text_from_image(image_path: Path) -> str:
    """
    Extrae texto de un archivo de imagen usando Tesseract OCR.
    """
    text = ""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
    except pytesseract.TesseractNotFoundError:
        raise HTTPException(status_code=500, detail="Tesseract OCR no está instalado o no se encuentra en el PATH. Por favor, instálalo.")
    except Exception as e:
        print(f"Error al extraer texto de imagen {image_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen con OCR: {e}")
    return text
```

### Propósito
Encapsula la lógica para extraer texto de archivos de imagen utilizando OCR.

### Razón de las Elecciones de Código
*   **`Image.open(image_path)`**: Carga la imagen usando Pillow.
*   **`pytesseract.image_to_string(img)`**: Realiza la operación OCR para extraer texto.
*   **Manejo de Errores Específico**: `pytesseract.TesseractNotFoundError` se maneja específicamente para dar un mensaje útil al usuario sobre la instalación de Tesseract. Las otras excepciones se manejan genéricamente.

### Pros y Contras
*   **Pros**:
    *   **Versatilidad**: Permite procesar CVs escaneados o en formato de imagen.
    *   **Potencia de Tesseract**: Tesseract es un motor OCR muy capaz.
*   **Contras**:
    *   **Dependencia Externa Obligatoria**: La necesidad de instalar Tesseract-OCR en el sistema es una barrera significativa.
    *   **Precisión Variable**: La calidad del texto extraído depende en gran medida de la calidad de la imagen (resolución, claridad, fuentes, rotación). Las imágenes de baja calidad producirán resultados pobres.
    *   **Lento**: El OCR puede ser un proceso computacionalmente intensivo y más lento que la extracción de texto de PDFs o DOCX.

### Posibles Mejoras
*   **Preprocesamiento de Imagen**: Antes de pasar la imagen a Tesseract, se podrían aplicar técnicas de preprocesamiento (escalado, binarización, eliminación de ruido, corrección de sesgo) para mejorar la precisión del OCR.
*   **Manejo de Idiomas**: Especificar el idioma del CV al llamar a `image_to_string` para mejorar la precisión del OCR si el CV no está en inglés.
*   **Detección de Texto por Regiones**: Para un análisis más avanzado, se podría usar técnicas de detección de regiones de texto para dirigir el OCR solo a áreas relevantes.

## 4. Lógica de Extracción de Información (`extract_info_from_text`)

```python
def extract_info_from_text(text: str) -> CVInfo:
    """
    Extrae información clave de un CV en formato de texto usando expresiones regulares.
    """
    name = None
    email = None
    phone = None

    # Expresión regular para email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        email = email_match.group(0)

    # Expresión regular para teléfono (ej. +XX XXX XXX XXXX, XXX XXX XXXX, etc.)
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3}[-.\s]?\d{4}|\d{7})", text)
    if phone_match:
        phone = phone_match.group(0)
    
    # Intento básico de extraer un nombre (esto es muy rudimentario y necesita mejora)
    # Buscar una línea que podría ser el nombre al principio del CV
    lines = text.split('\n')
    if lines:
        first_line = lines[0].strip()
        # Asumiendo que el nombre es la primera línea que parece un nombre propio
        if len(first_line.split()) <= 4 and re.match(r"^[A-Z][a-zA-Z\s.-]*$", first_line):
             name = first_line

    return CVInfo(name=name, email=email, phone=phone, full_text=text)
```

### Propósito
Esta función toma el texto extraído de un CV y utiliza expresiones regulares para identificar y extraer piezas específicas de información, como el nombre, correo electrónico y número de teléfono.

### Razón de las Elecciones de Código

*   **Variables Inicializadas a `None`**: Esto asegura que si no se encuentra un patrón, el campo correspondiente en el `CVInfo` seguirá siendo `None`, lo cual es manejado por el modelo Pydantic.
*   **Expresiones Regulares (`re.search`)**: Se utilizan para buscar patrones específicos en el texto.
    *   **Email**: La regex para email es bastante estándar y robusta para la mayoría de los formatos de correo electrónico.
    *   **Teléfono**: La regex para teléfono intenta ser flexible para capturar varios formatos comunes de números de teléfono, incluyendo códigos de país opcionales, paréntesis y diferentes separadores.
    *   **Nombre (Enfoque Rudimentario)**: La estrategia para el nombre es muy simple: busca la primera línea del CV que podría parecer un nombre propio (capitalización inicial, no más de 4 palabras). Esto es una simplificación extrema.
*   **`match.group(0)`**: Si se encuentra una coincidencia, `group(0)` devuelve la cadena completa que coincidió con el patrón.

### Pros y Contras
*   **Pros**:
    *   **Simple y Rápido**: Para la extracción de patrones bien definidos como emails y teléfonos, las expresiones regulares son muy eficientes.
    *   **Control Explícito**: Permiten un control exacto sobre los patrones que se buscan.
*   **Contras**:
    *   **Falta de Contexto**: Las expresiones regulares no entienden el contexto semántico del texto. Por ejemplo, un número que parezca un teléfono pero sea parte de una dirección postal se extraería incorrectamente.
    *   **Nombre Rudimentario**: La extracción del nombre es muy limitada y probablemente fallará en muchos CVs reales. No considera la posición del nombre, la presencia de títulos, ni la variación en los formatos de nombres.
    *   **Escalabilidad Limitada**: Para extraer información más compleja como experiencia laboral, educación, habilidades, fechas, etc., las expresiones regulares se vuelven extremadamente complejas y frágiles. Se requerirían enfoques de Procesamiento de Lenguaje Natural (NLP) más avanzados.
    *   **Mantenimiento**: A medida que los patrones de CVs varían, mantener y actualizar un gran conjunto de expresiones regulares puede ser tedioso.

### Posibles Mejoras
*   **Extracción de Nombre Robusta**: Implementar heurísticas más avanzadas o usar librerías de NLP (ej. `spaCy`, `NLTK`) para el Reconocimiento de Entidades Nombradas (NER) que puedan identificar nombres de personas con mayor fiabilidad. Esto podría implicar buscar patrones de encabezado o usar modelos pre-entrenados.
*   **Extracción de Experiencia/Educación/Habilidades**: Utilizar técnicas de NLP como el análisis de secciones, extracción de frases clave, o incluso modelos de machine learning (si se dispone de datos etiquetados) para identificar y estructurar estas secciones.
*   **Normalización de Datos**: Una vez extraídos, los datos podrían necesitar normalización (ej. formatos de fecha, unificación de nombres de habilidades).
*   **Validación Cruzada**: Validar la información extraída (ej. verificar la validez de un email).

## 5. Endpoints de la API (`/` y `/cv`)

Esta sección define las rutas accesibles a través de la API.

### 5.1. `@app.get("/")`

```python
@app.get("/")
async def read_root():
    return {"message": "Hello World, from fastAPI-cv!"}
```

### Propósito
Un endpoint de "saludo" simple para verificar que la API está funcionando.

### Razón de las Elecciones de Código
*   **`@app.get("/")`**: Define un manejador para solicitudes GET a la ruta raíz.
*   **`async def read_root():`**: Función asíncrona, estándar en FastAPI para manejar operaciones I/O bloqueantes de manera eficiente.
*   **`return {"message": ...}`**: Devuelve un diccionario que FastAPI serializa automáticamente a JSON.

### Pros y Contras
*   **Pros**:
    *   **Verificación Rápida**: Proporciona una forma inmediata de saber si la aplicación se ha desplegado correctamente.
    *   **Simplicidad**: Un ejemplo claro y conciso del funcionamiento básico de FastAPI.
*   **Contras**:
    *   **No Funcional**: No aporta funcionalidad directa al objetivo principal del proyecto.

### Posibles Mejoras
*   Podría eliminarse una vez que se haya probado que la API funciona.

### 5.2. `@app.post("/cv")`

```python
@app.post("/cv")
async def upload_cv(file: UploadFile = File(...)):
    try:
        # Sanitizar el nombre del archivo para evitar ataques de path traversal
        filename = Path(file.filename).name
        file_path = TEMP_CV_DIR / filename

        # Guardar el archivo temporalmente
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Detectar el tipo MIME
        detected_mime_type = get_mime_type(file_path)

        if not detected_mime_type:
            return {"filename": filename, "status": "Uploaded, MIME type not detected. Proceed with caution.", "detected_mime_type": None}
        
        # Procesar el archivo según su tipo MIME
        extracted_text = None
        if detected_mime_type == "application/pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif detected_mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx(file_path)
        elif detected_mime_type.startswith("image/"): # Procesa cualquier tipo de imagen
            extracted_text = extract_text_from_image(file_path)

        # Eliminar el archivo temporal después de procesar
        os.remove(file_path)
        
        if extracted_text:
            cv_info = extract_info_from_text(extracted_text)
            return cv_info
        else:
            return {"filename": filename, "detected_mime_type": detected_mime_type, "message": "Tipo de archivo no soportado aún para extracción de texto o error en la extracción."}

    except Exception as e:
        # Asegurarse de eliminar el archivo temporal en caso de error
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error al subir o procesar el archivo: {e}")
```

### Propósito
Este es el endpoint central de la API. Permite a los usuarios subir un archivo de CV, lo procesa según su tipo y devuelve la información extraída en formato JSON.

### Razón de las Elecciones de Código

*   **`@app.post("/cv")`**: Define un manejador para solicitudes POST a la ruta `/cv`. POST es el método HTTP adecuado para enviar datos al servidor para su creación o procesamiento.
*   **`file: UploadFile = File(...)`**: Esta es la forma estándar de FastAPI para manejar la subida de archivos.
    *   `UploadFile`: Es una clase de Starlette/FastAPI que proporciona una interfaz asíncrona para leer el archivo subido, incluyendo `filename`, `content_type` y el método `file` (un objeto de tipo `SpooledTemporaryFile`).
    *   `File(...)`: Indica que este parámetro debe extraerse de los datos de formulario/multipart de la solicitud.
*   **Manejo de Archivos Temporales**:
    *   `filename = Path(file.filename).name`: **Saneamiento crítico del nombre de archivo**. `Path(...).name` asegura que solo se toma el nombre base del archivo, previniendo ataques de "path traversal" (ej. un usuario subiendo un archivo llamado `../../etc/passwd`).
    *   `file_path = TEMP_CV_DIR / filename`: Construye la ruta completa para guardar el archivo temporalmente.
    *   `with file_path.open("wb") as buffer: shutil.copyfileobj(file.file, buffer)`: Guarda el contenido del archivo subido en el disco. `shutil.copyfileobj` es eficiente para copiar streams.
*   **Detección y Procesamiento Condicional**:
    *   `detected_mime_type = get_mime_type(file_path)`: Obtiene el tipo MIME del archivo.
    *   La serie de `if/elif` statements dirige el archivo al extractor de texto apropiado (`extract_text_from_pdf`, `extract_text_from_docx`, `extract_text_from_image`) basado en el tipo MIME detectado.
*   **`os.remove(file_path)`**: **Limpieza**. Una vez que el archivo ha sido procesado (o si no es un tipo soportado), se elimina del directorio temporal. Esto es crucial para la seguridad y para evitar el consumo de espacio en disco.
*   **`extract_info_from_text(extracted_text)`**: Llama a la función de extracción de información una vez que se ha obtenido el texto completo.
*   **`return cv_info`**: Devuelve el objeto `CVInfo` (Pydantic), que FastAPI serializa automáticamente a JSON.
*   **Manejo de Errores General**:
    *   `try...except Exception as e`: Un bloque `try-except` general captura cualquier error inesperado durante el proceso.
    *   `if file_path.exists(): os.remove(file_path)`: Asegura que el archivo temporal se elimine incluso si ocurre un error durante el procesamiento.
    *   `raise HTTPException(status_code=500, detail=f"Error al subir o procesar el archivo: {e}")`: Devuelve un error HTTP 500 al cliente con detalles del problema.

### Pros y Contras
*   **Pros**:
    *   **Modularidad**: Separa claramente la lógica de recepción de archivos, guardado, detección de tipo, extracción de texto y extracción de información.
    *   **Robustez**: Incluye saneamiento de nombres de archivo y limpieza de archivos temporales.
    *   **Extensibilidad**: Fácil añadir soporte para nuevos tipos de archivo simplemente añadiendo un `elif` y una nueva función de extracción.
    *   **Documentación Automática**: FastAPI genera automáticamente una interfaz de usuario para probar este endpoint, mostrando los tipos de archivo esperados y la estructura de la respuesta.
*   **Contras**:
    *   **Manejo de Errores**: El `except Exception as e` es muy genérico. Para un sistema de producción, sería mejor capturar excepciones más específicas y manejarlas de manera diferenciada (ej. `FileNotFoundError`, errores de validación, etc.).
    *   **Mime Type Inferencia**: La dependencia de `mimetypes.guess_type` puede ser una debilidad si se suben archivos con tipos MIME incorrectos o engañosos.
    *   **Bloqueo**: Aunque FastAPI es asíncrono, las operaciones de extracción de texto (`fitz`, `python-docx`, `pytesseract`) son bloqueantes. Para una alta concurrencia, esto podría ser un cuello de botella. Se podrían ejecutar en un `ThreadPoolExecutor` para no bloquear el bucle de eventos principal (FastAPI lo hace automáticamente para funciones `def` normales dentro de endpoints `async def`, pero es importante ser consciente).

### Posibles Mejoras
*   **Validación de Contenido**: Complementar la detección de tipo MIME por extensión con una validación de "magic bytes" (primeros bytes del archivo) para verificar el tipo real del archivo y evitar el procesamiento de archivos maliciosos o incorrectos.
*   **Límites de Tamaño**: Implementar límites de tamaño de archivo para evitar ataques de denegación de servicio (DoS) por archivos excesivamente grandes.
*   **Asincronía en Extractores**: Para los extractores que son operaciones I/O o CPU intensivas, considerar ejecutarlos en un pool de hilos (`run_in_threadpool` de `starlette.concurrency`) si la aplicación va a manejar mucha concurrencia y los extractores son funciones síncronas. FastAPI ya maneja esto implícitamente, pero es una consideración.
*   **Logging Mejorado**: Mejorar el `print` de errores por un sistema de logging más robusto.

---

```