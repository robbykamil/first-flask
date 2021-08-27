from flask import Flask, request, redirect, url_for, render_template, Response
import cv2
import os
#from numpy.lib.shape_base import expand_dims
#import tensorflow as tf
#import numpy as np


#from PIL import Image
#from google.cloud import storage

app = Flask(__name__, template_folder="template")



def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('isyaratku.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/get-image', methods=['GET', 'POST'])
def get_image():
    if request.method == 'POST':
        nama = request.form.get("huruf")
        filepath = nama + ".png"
        URL = "https://storage.googleapis.com/bismillahdetect/{}".format(filepath)
        return render_template('get-translate.html', nama=nama, pict=URL)
    else:
        redirect(url_for('translate'))

@app.route('/detect')
def detect():
    return render_template('detect.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
