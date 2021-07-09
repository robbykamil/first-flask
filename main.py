import os
import base64
import io

#import image
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for
from google.cloud import storage


app = Flask(__name__, template_folder="template")

# Configure this environment variable via app.yaml
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']

storage_client = storage.Client()

def download_pict():
    nama = request.form.get("huruf")
    filepath = "/" + nama + ".png"
    
    buc = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = buc.get_blob(filepath)
    url_pict = blob.download_as_bytes()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/translate')
def translate():
    return render_template("translate.html")

@app.route('/get-image', methods=['POST'])
def get_image():
    filename = download_pict()
    return render_template("get-translate.html", pict=filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

