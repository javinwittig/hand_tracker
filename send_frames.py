import time
import subprocess
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, Response
import requests

app = Flask(__name__)

# Kameraspezifikationen
WIDTH, HEIGHT = 640, 480
FRAME_SIZE = int(WIDTH * HEIGHT * 1.5)

DETECTION_RESULT = None


SERVER_URL = "http://192.168.178.88:8000/upload_frame"



def generate_frames():
    cmd = [
        "rpicam-vid", "-t", "0",
        "--width", str(WIDTH), "--height", str(HEIGHT),
        "--framerate", "15", "--codec", "yuv420",
        "--rotation", "180", "-o", "-", "-n"
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    frame_count = 0


    try:
        while True:
            raw_data = process.stdout.read(FRAME_SIZE)
            if len(raw_data) != FRAME_SIZE:
                print("error")
                break

            yuv = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(HEIGHT * 1.5), WIDTH))
            frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
            frame = cv2.flip(frame, 1)

            frame_count += 1


            # ERST encodieren...
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 65])
            frame_bytes = buffer.tobytes()

            # ...DANN als bytes verschicken
            try:
                requests.post(SERVER_URL, data=frame_bytes, timeout=1)
            except requests.exceptions.RequestException as e:
                print(f"Senden fehlgeschlagen: {e}")
    finally:
        print("")
        process.terminate()


if __name__ == '__main__':
    print("Starting ...")
    generate_frames()