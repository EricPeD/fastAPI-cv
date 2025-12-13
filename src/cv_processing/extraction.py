from pathlib import Path
import fitz
from docx import Document
from PIL import Image
import pytesseract
from src.config import logger

def extract_text_from_pdf(pdf_path: Path) -> str:
    text = ""
    try:
        document = fitz.open(pdf_path)
        for page in document:
            text += page.get_text()
        document.close()
    except Exception as e:
        logger.error(f"Error al extraer texto de PDF {pdf_path.name}: {e}")
    return text


def extract_text_from_docx(docx_path: Path) -> str:
    text = ""
    try:
        document = Document(docx_path)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        logger.error(f"Error al extraer texto de DOCX {docx_path.name}: {e}")
    return text


def extract_text_from_image(image_path: Path) -> str:
    text = ""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
    except pytesseract.TesseractNotFoundError:
        logger.error(
            "Error: Tesseract OCR no está instalado o no se encuentra en el PATH."
        )
    except Exception as e:
        logger.error(f"Error al extraer texto de imagen {image_path.name}: {e}")
    return text
