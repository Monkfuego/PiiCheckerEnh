import os
from docx import Document
import PyPDF2
from pdfminer.high_level import extract_text as pdfminer_extract_text
from bs4 import BeautifulSoup
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from PIL import Image, ImageDraw
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

subscription_key = "da743008b85d4f16bdb6035f8ed89123"
endpoint = "https://piidetectivecv.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def read_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        return read_text_from_txt(file_path)
    elif ext == '.docx':
        return read_text_from_docx(file_path)
    elif ext == '.pdf':
        return read_text_from_pdf(file_path)
    elif ext == '.html' or ext == '.htm':
        return read_text_from_html(file_path)
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
        return read_text_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def read_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_text_from_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def read_text_from_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            for page_num in range(reader.getNumPages()):
                text += reader.getPage(page_num).extractText()
        if not text.strip():  # If PyPDF2 fails, use pdfminer
            text = pdfminer_extract_text(file_path)
    except Exception as e:
        text = pdfminer_extract_text(file_path)
    return text

def read_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def read_text_from_image(image_path):
    with open(image_path, "rb") as image_stream:
        ocr_result = computervision_client.read_in_stream(image_stream, raw=True)
    
    operation_location_remote = ocr_result.headers["Operation-Location"]
    operation_id = operation_location_remote.split("/")[-1]

    while True:
        get_text_results = computervision_client.get_read_result(operation_id)
        if get_text_results.status not in ['notStarted', 'running']:
            break
    if get_text_results.status == OperationStatusCodes.succeeded:
        extracted_text = []
        for text_result in get_text_results.analyze_result.read_results:
            for line in text_result.lines:
                extracted_text.append(line.text)
        return "\n".join(extracted_text)
    else:
        return "Text extraction failed."
