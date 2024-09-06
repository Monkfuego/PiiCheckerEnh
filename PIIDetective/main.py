from flask import Flask, request, render_template
import os
from pii_detective import remove_first_slash , detector_main , pii_detect_layer2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp'

@app.route("/")
def main():
    return render_template("main.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    if file:
        # Save the file to the temporary folder
        print(file.filename)
        file_path = "temp" + str(file.filename)
        file_path = remove_first_slash(file_path)
        file.save(file_path)
        
        # Call your PII detection function here
        result = pii_detect_layer2(file_path)

        return result

if __name__ == "__main__":
    app.run(debug=True)
