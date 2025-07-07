import os
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename

from parser.extractor import extract_text_from_pdf, extract_details
from database import Candidate, SessionLocal

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']
        if file.filename == '':
            return "No file selected"

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text_from_pdf(filepath)
        data = extract_details(text)

        db = SessionLocal()
        candidate = Candidate(**data)
        db.add(candidate)
        db.commit()
        db.close()

        return f"Resume for {data['name']} parsed and stored."

    return render_template('upload.html')
