import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image
import os
import fitz  
import docx  
import xlrd  
import cv2  

# Put the trained models for each document type
models = {
    'Aadhar Card': keras.models.load_model('aadhar_card_model.py'),
    #'Pan Card': keras.models.load_model('pan_card_model.h5'),
    #'Voter Id': keras.models.load_model('voter_id_model.h5'),
    #'Passport': keras.models.load_model('passport_model.h5'),
    #'Driver License': keras.models.load_model('driver_license_model.h5'),
    #'NREGA Job Card': keras.models.load_model('nrega_job_card_model.h5')
}

pii_regex = {
    'GSTIN': re.compile(r'\b\d{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{3}\b'),
    'PhoneNumber_India': re.compile(r'\b(\+91[\-\s]?)?[6789]\d{9}\b'),
    'Email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    'BankAccount_India': re.compile(r'\b\d{9,18}\b'),
    'CreditCard': re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b'),
    'IPv4': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
    'IPv6': re.compile(r'\b([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)\b'),
    'IFSC': re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b'),
    'VehicleRegistration_India': re.compile(r'\b[A-Z]{2}[0-9]{2}[A-Z]{1,2}\d{4}\b'),
    'NPS_PRAN': re.compile(r'\b\d{12}\b')
}

doc_pii_regex = {
    'Aadhar Card': re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b'),
    'Pan Card': re.compile(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'),
    'Voter Id': re.compile(r'\b[A-Z]{3}[0-9]{7}\b'),
    'Passport': re.compile(r'\b[A-Z]{1}\d{7}\b'),
    'Driver License': re.compile(r'\b[A-Z]{2}\d{2}\s\d{11}\b'),
    'NREGA Job Card': re.compile(r'\b\d{2}\s\d{4}\s\d{4}\s\d{4}\b')
}

def detect_document(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image_array = img_to_array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    predictions = {}
    for doc_type, model in models.items():
        prediction = model.predict(image_array)
        predictions[doc_type] = np.argmax(prediction)

    detected_docs = [doc_type for doc_type, prediction in predictions.items() if prediction == 1]
    return detected_docs

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        with fitz.open(file_path) as doc:
            text = ''
            for page in doc:
                text += page.getText()
            return text
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = ''
        for para in doc.paragraphs:
            text += para.text
        return text
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        workbook = xlrd.open_workbook(file_path)
        text = ''
        for sheet in workbook.sheets():
            for row in range(sheet.nrows):
                                for col in range(sheet.ncols):
                    text += str(sheet.cell_value(row, col)) + ' '
        return text
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg') or file_path.endswith('.png'):
        image = cv2.imread(file_path)
        text = pytesseract.image_to_string(Image.fromarray(image))
        return text
    else:
        with open(file_path, 'r') as file:
            return file.read()

def detect_pii(text):
    pii_detected = {}
    for pii_type, regex in pii_regex.items():
        matches = regex.findall(text)
        if matches:
            pii_detected[pii_type] = matches
    return pii_detected

def detect_doc_pii(text, doc_type):
    pii_detected = {}
    for pii_type, regex in doc_pii_regex.items():
        if pii_type == doc_type:
            matches = regex.findall(text)
            if matches:
                pii_detected[pii_type] = matches
    return pii_detected

def main():
    file_path = input("Enter the file path: ")
    text = extract_text_from_file(file_path)
    detected_docs = detect_document(file_path)
    if detected_docs:
        for doc_type in detected_docs:
            pii_detected = detect_doc_pii(text, doc_type)
            if pii_detected:
                print(f"PII detected in {doc_type}: {pii_detected}")
            else:
                print(f"No PII detected in {doc_type}")
    else:
        print("No document detected")


