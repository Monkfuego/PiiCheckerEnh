import os
from flask import *
from pii_detective import pii_detect_layer1,pii_detect_layer2
server = Flask(__name__)
@server.route('/process_image', methods=['GET'])
def process_image_endpoint():
    file = request.files['file']
    # Save the file to a temporary location
    temp_file_path = '/tmp/temp_image.jpg'
    file.save(temp_file_path)
    
    # Call your Python function, passing the temporary file path as input
    result = pii_detect_layer1(temp_file_path)
    
    # Remove the temporary file
    os.remove(temp_file_path)
    return "<p>hi</p>"
if __name__ == "__main__":
    server.run(debug = False)
