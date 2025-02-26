from flask import Flask, render_template, request, redirect, url_for
import os
import pytesseract  
from PIL import Image  

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory inventory
inventory = {
    "paracetamol": {"price": 1.50, "stock": 100},
    "citagen": {"price": 3.00, "stock": 50},
    "dolo": {"price": 2.00, "stock": 75},
    "hifenac": {"price": 2.50, "stock": 60},
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patient_name = request.form['patient_name']

        if 'prescription_image' not in request.files:
            return redirect(request.url)

        file = request.files['prescription_image']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Saving the uploaded file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Process the image using OCR
            try:
                prescription_text = pytesseract.image_to_string(Image.open(filename))
            except Exception as e:
                return f"Error during OCR: {str(e)}"  # Handle OCR errors

            # Process the prescription
            order, unmatched_items = process_prescription(prescription_text, inventory)

            # Delete the uploaded image after processing to save space.
            os.remove(filename)

            return render_template('results.html',
                                   patient_name=patient_name,
                                   order=order,
                                   unmatched_items=unmatched_items,
                                   prescription_text=prescription_text)  # Pass OCR text to results

        return redirect(request.url)

    return render_template('index.html')


def process_prescription(prescription_text, inventory):
    prescribed_medicines = [med.strip().lower() for line in prescription_text.split('\n')
                              for part in line.split(',')
                              for med in part.split()
                              if med.strip()] 
    order = {}
    unmatched_items = []

    for medicine_name in prescribed_medicines:
        if medicine_name in inventory:
            if inventory[medicine_name]['stock'] > 0:
                order[medicine_name] = {
                    "price": inventory[medicine_name]['price'],
                    "quantity": 1
                }
                inventory[medicine_name]['stock'] -= 1
            else:
                unmatched_items.append(f"{medicine_name} (Out of Stock)")
        else:
            unmatched_items.append(medicine_name)
    return order, unmatched_items

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
