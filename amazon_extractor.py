import pytesseract
from pdf2image import convert_from_path
import logging


def extract_text_from_amazon_pdf(pdf_path):
    """
    Extracts text from a PDF file using OCR.
    
    Args:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text from the PDF.
    """
    try: 
        # Convert PDF to images
        images = convert_from_path(pdf_path)

        # Apply OCR to each image and collect text
        ocr_text = ""
        for image in images:
            text = pytesseract.image_to_string(image, lang="eng")
            ocr_text += text + "\n"

    except FileNotFoundError:
        logging.error(f"File not found: {pdf_path}")
        return ""
    except Exception as e:
        logging.error(f"An error occurred while extracting text from the PDF: {e}")
        return ""

    return ocr_text