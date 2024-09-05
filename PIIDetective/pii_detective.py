from keras import models
from processing import preprocess_image
from file_reader import output_folder, read_text_from_file, image_extraction
import os
import numpy as np
from pii_regex import pii_regex, doc_pii_regex 

def pii_detect_layer1(file):
    results = []
    
    for label, pattern in {**pii_regex, **doc_pii_regex}.items():
        matches = pattern.findall(read_text_from_file(file))
        if matches:
            for match in matches:
                results.append((label, match))
    return results

def pii_detect_layer2(file):
    extracted_images = []
    model = models.load_model('aadhar_card_model.keras')
    
    # Iterate over extracted images and make predictions
    for filename in os.listdir(output_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            extracted_images.append(filename)
            img_path = os.path.join(output_folder, filename)
            img_array = preprocess_image(img_path)  # Preprocess the image
            
            # Predict for each preprocessed image
            for img in img_array:
                prediction = model.predict(np.expand_dims(img, axis=0))
                predicted_class = np.argmax(prediction)
                print(f"Predicted class for {filename}: {predicted_class}")
