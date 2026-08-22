from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import time
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions

app = Flask(__name__)

# --- Kamera einrichten ---
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()
time.sleep(1)  # Belichtung einpendeln lassen

# --- MediaPipe Hand Landmarker einrichten ---
base_options = BaseOptions(model_asset_path="hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_tracking_confidence=0.5,
)
detector = vision.HandLandmarker.create_from_options(options)

frame_timestamp_ms = 0

def generate_frames():
    global frame_timestamp_ms
    while True:
        img = picam2.capture_array()  # RGB, numpy-Array direkt von der Kamera

        # MediaPipe braucht ein eigenes Image-Objekt
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

        # Timestamp muss aufsteigend sein
        frame_timestamp_ms += 33  # ~30 FPS
        result = detector.detect_for_video(mp_image, frame_timestamp_ms)

        # Für Anzeige im Browser zu BGR konvertieren
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.hand_landmarks:
            h, w, _ = img.shape
            for hand_landmarks in result.hand_landmarks:
                # alle 21 Punkte einzeichnen
                for lm in hand_landmarks:
                    x_px, y_px = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (x_px, y_px), 3, (0, 255, 0), -1)

                # Zeigefingerspitze hervorheben (Landmark Index 8)
                tip = hand_landmarks[8]
                x_px, y_px = int(tip.x * w), int(tip.y * h)
                cv2.circle(img, (x_px, y_px), 8, (0, 0, 255), -1)

        # Bild als JPEG encodieren für den Stream
        success, buffer = cv2.imencode(".jpg", img)
        if not success:
            continue

        frame = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/")
def index():
    return "<html><body><h1>Hand Tracking Live</h1><img src='/video'></body></html>"

@app.route("/video")
def video():
    return Response(generate_frames(),
                     mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)