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
        name = request.form.get("huruf")
        filepath = name + ".png"

        buc = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
        blob = buc.blob(filepath)
        filename = blob.download_to_filename(filepath)

        im = Image.open(filename)
        data = io.BytesIO()
        im.save(data, "PNG")
        encoded_img_data = base64.b64encode(data.getvalue())

        return render_template("get-translate.html", nama=name, pict=encoded_img_data.decode('utf-8'))
    else:
        return redirect(url_for(translate))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

