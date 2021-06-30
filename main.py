import re
import io, os
import cloudstorage

from flask import Flask, request, render_template, #send_file
from google.appengine.api import app_identity
from google.cloud import storage


app = Flask(__name__, template_folder="template")


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/text', methods=['GET'])
def text():
    return render_template("text.html")


@app.route('/get-text', methods=['POST'])
def user_get_text():
  
  nama = request.form.get("nama")
  
  BUCKET_NAME = '/' + os.environ.get('image_language', app_identity.get_default_gcs_bucket_name())
  ####filename = ""####
  ####filepath = os.path.join(BUCKET_NAME, filename)####
  
  storage_client = storage.Client()
  blobs = storage_client.list_blobs(image_language, prefix='Colored/', delimiter='/')
  
  for blob in blobs:
    if nama in blob:
      filepath = os.path.join(BUCKET_NAME, blob)
      gcs_file = cloudstorage.open(filepath)
      contents = gcs_file.read()
      gcs.file.close
      
      filename = send_file(io.BytesIO(contents), mimetype='image/png')
      break

  return render_templat("get-text.html", name=nama, pict=filename)


