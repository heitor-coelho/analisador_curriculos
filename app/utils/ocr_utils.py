import pytesseract
from PIL import Image, UnidentifiedImageError
import io
import fitz  # PyMuPDF

def extract_text_from_image(file_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(file_bytes))
        return pytesseract.image_to_string(image)
    except UnidentifiedImageError:
        raise ValueError("Arquivo de imagem inválido ou corrompido")
    except Exception as e:
        raise RuntimeError(f"Erro ao extrair texto da imagem: {e}")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Erro ao extrair texto do PDF: {e}")

def extract_text(filename: str, file_bytes: bytes) -> str:
    filename_lower = filename.lower()
    if filename_lower.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(file_bytes)
    elif filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {filename_lower}")
