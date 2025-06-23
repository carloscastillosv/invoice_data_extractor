from amazon_extractor import extract_text_from_amazon_pdf
from openai_utils import call_openai_assistant
import logging
import os

logging.basicConfig(
    filename="logger.log",   # Log file path
    level=logging.INFO,      # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    filemode="a"  # Use "w" to overwrite each time
)

AMAZON_FOLDER = os.getenv("AMAZON_FOLDER")

def main():
    # Folder containing the PDF files
    pdf_folder = AMAZON_FOLDER

    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        logging.info(f"Extracting text from PDF: {pdf_path}")
        extracted_text = extract_text_from_amazon_pdf(pdf_path)
        openai_response = call_openai_assistant(pdf_text=extracted_text)
        print(f"Response from OpenAI for {pdf_file}:\n{openai_response}\n")
        logging.info(f"Processed PDF: {pdf_file}")


if __name__ == "__main__":
    main()