# PrescriptoMate

A Flask-based application that processes handwritten prescription images using Tesseract OCR, matches extracted medicines against an in-memory inventory, and generates an order for the patient.

# Features
✅ Upload handwritten prescription images
✅ Extract text using Tesseract OCR
✅ Match medicines with inventory
✅ Generate an order for the patient
✅ Display unmatched medicines

# Installation & Setup
**Prerequisites**
Ensure you have the following installed:
-Python 3.x
-pip (Python package manager)
-Flask (for backend development)
-Tesseract OCR (for text extraction)
-Web Browser (Google Chrome, Firefox, Safari,etc.)

**Clone the Repository**

**Set Up a Virtual Environment**
Create virtual environment
python -m venv venv  

Activate virtual environment
-On Windows:
venv\Scripts\activate  
-On macOS/Linux:
source venv/bin/activate

**Install Dependencies**
pip install -r requirements.txt

**Install Tesseract OCR**
Windows
-Download Tesseract.
-Install it and note the installation path (e.g., C:\Program Files\Tesseract-OCR).

Linux (Debian/Ubuntu)
sudo apt update
sudo apt install tesseract-ocr

Mac (Using Homebrew)
brew install tesseract

**Run the Flask App**
python app.py
The app will start on http://127.0.0.1:5000/

# Usage
1. Open the web app in your browser.
2. Enter the patient's name.
3. Upload a handwritten prescription image (.jpg, .png, etc.).
4. Click Submit to process the image.
5. View the extracted medicines, matched orders, and any unmatched items.

# Project Structure
/prescripomate
 ├── /uploads              # Stores uploaded images (temporary)
 ├── app.py                # Main Flask application
 ├── templates/            # HTML templates for frontend
 ├── static/               # CSS, JavaScript, and assets
 ├── requirements.txt      # List of dependencies
 ├── README.md             # Documentation

# Future Enhancements
✅ PostgreSQL database integration for persistent inventory storage
✅ Improved OCR with AI models for better accuracy
✅ Enhanced UI/UX with modern frontend frameworks
