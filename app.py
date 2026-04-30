from flask import Flask, render_template, request
from analyser import extract_text_from_pdf, analyse
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyse', methods = ['POST'])
def analyse_resume():
    file = request.files['resume']
    job_desc = request.form['job_desc']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    resume_text = extract_text_from_pdf(file_path)
    result = analyse(resume_text, job_desc)

    return render_template('result.html', result=result)
if __name__ == '__main__':
    app.run(debug=True)