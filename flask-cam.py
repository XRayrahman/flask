from flask import Flask, render_template, Response, request
import cv2
import subprocess
import os
import random

app = Flask(__name__)

pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "jpegdec",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "appsink sync=false"
                       ])

def gen_frames():
    camera = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""    
    return render_template('index.html')

if __name__ == '__main__':
    port = 5000 + random.randint(0,999)
    print(port)
    app.run(host="0.0.0.0",debug=True, port=port)
