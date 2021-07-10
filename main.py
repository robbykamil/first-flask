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


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/translate')
def translate():
    return render_template("translate.html")

@app.route('/get-image', methods=['GET', 'POST'])
def get_image():
    if request.method == 'POST':
        nama = request.form.get("huruf")
        return redirect(url_for("pict_download", nama=nama))
    else:
        return render_template("get-translate.html")
    
@app.route('/get-image/<nama>')
def pict_download(nama):
    filepath = nama + ".png"
    
    buc = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = buc.blob(filepath)
    pict = blob.download_as_bytes()
    
    return pict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

