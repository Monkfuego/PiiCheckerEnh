from keras import models
from processing import preprocess_image
from file_reader import read_text_from_file, image_extraction,output_folder
import os
import numpy as np
from pii_regex import pii_regex, doc_pii_regex 

def pii_detect_layer1(file):
    results = []
    file_content = read_text_from_file(file)

    lines = file_content.split('\n')
    for line_number, line in enumerate(lines, start=1):
        for label, pattern in {**pii_regex, **doc_pii_regex}.items():
            matches = pattern.findall(line)
            if matches:
                for match in matches:
                    results.append((label, match, line_number, line.strip()))
    
    return results

def pii_detect_layer2(file):
    extracted_images = []
    model = models.load_model('aadhar_card_model.keras')
    image_extraction(file)
    # Iterate over extracted images and make predictions
    for filename in os.listdir(output_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            extracted_images.append(filename)
            img_path = os.path.join(output_folder, filename)
            img_array = preprocess_image(img_path)  # Preprocess the image
           
            for img in img_array:
               
                prediction = model.predict(np.expand_dims(img, axis=0))
                predicted_class = np.argmax(prediction)
                
            if predicted_class==1:
                return filename
            else:
                return None

def detector_main(file):
    ext = os.path.splitext(file)[1].lower()
    if ext == '.jpg' or ext == '.jpeg' or ext == '.png':
        pii_detect_layer2(file)
    elif ext == '.txt' or '.docx' or '.pdf' or '.html' or '.htm' or '.csv' or '.xml' or '.json' or '.xlsx':
        pii_detect_layer1(file)
        pii_detect_layer2(file)  
    else:
        return (f"Unsupported file extension: {ext}")
