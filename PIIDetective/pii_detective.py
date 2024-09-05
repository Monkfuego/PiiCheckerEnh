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

from keras import models
from processing import preprocess_image
from file_reader import read_text_from_file, image_extraction,output_folder
import os
import numpy as np
from pii_regex import pii_regex, doc_pii_regex 
print(str(output_folder))
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

