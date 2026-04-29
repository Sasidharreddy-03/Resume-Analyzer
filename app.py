from flask import Flask, render_template, request
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route('/')
def home():
    return "resume analyzer is live"
if __name__ == '__main__':
    app.run(debug = True)
    