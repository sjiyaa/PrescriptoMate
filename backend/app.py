from flask import Flask, render_template, request, redirect, url_for
import pytesseract
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def preprocess_image(image_path):
    """Preprocess the image to enhance OCR accuracy."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Apply noise removal
    denoised = cv2.fastNlMeansDenoising(thresh, None, 30, 7, 21)
    
    # Apply morphological transformations
    kernel = np.ones((2,2), np.uint8)
    processed = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
    
    return processed

def extract_text(image_path):
    """Extract text from the preprocessed image using Tesseract."""
    processed_image = preprocess_image(image_path)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed.png')
    cv2.imwrite(temp_path, processed_image)  # Save processed image
    
    text = pytesseract.image_to_string(processed_image, config='--psm 6')
    return text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'prescription_image' not in request.files:
            return redirect(request.url)
        file = request.files['prescription_image']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            extracted_text = extract_text(file_path)
            medicines = parse_medicines(extracted_text)
            return render_template('results.html', patient_name=request.form['patient_name'], order=medicines)
    
    return render_template('index.html')

def parse_medicines(text):
    all_medicines = {
        'paracetamol': {'price': 1.5, 'in_stock': True},
        'dolo': {'price': 2.0, 'in_stock': True},
        'crocin': {'price': 3.0, 'in_stock': True},
        'okacet': {'price': 2.5, 'in_stock': True}
    }

    detected_medicines = text.lower().split()
    
    # Filtering only available medicines
    available_medicines = {
        med: details for med, details in all_medicines.items()
        if med in detected_medicines and details['in_stock']
    }

    return available_medicines


if __name__ == '__main__':
    app.run(debug=True)
