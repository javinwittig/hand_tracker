import math
import os
import cv2
import mediapipe as mp
from dotenv import load_dotenv

load_dotenv()

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = os.getenv("MODEL_PATH", "hand_landmarker.task")

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE
)
landmarker = HandLandmarker.create_from_options(options)  # einmalig!

# Verbindungen zwischen Landmarks fürs Zeichnen des Handskeletts.
# Fest codiert: in dieser mediapipe-Version existiert das solutions-Modul
# gar nicht (bestätigt durch ImportError), daher kein Fallback-Versuch mehr.
HAND_CONNECTIONS = [
    # Daumen
    (0, 1), (1, 2), (2, 3), (3, 4),
    # Zeigefinger
    (0, 5), (5, 6), (6, 7), (7, 8),
    # Mittelfinger
    (9, 10), (10, 11), (11, 12),
    # Ringfinger
    (13, 14), (14, 15), (15, 16),
    # Kleiner Finger
    (0, 17), (17, 18), (18, 19), (19, 20),
    # Handfläche (verbindet die Finger-Ansätze untereinander)
    (5, 9), (9, 13), (13, 17),
]


def analyze_frame(frame):
    height, width = frame.shape[:2]

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result = landmarker.detect(mp_image)

    if not result.hand_landmarks:
        return {"found": False}

    landmarks = result.hand_landmarks[0]

    # Alle 21 Landmarks in Pixelkoordinaten (für Zeichnen + weitere Analyse)
    landmarks_px = [(int(lm.x * width), int(lm.y * height)) for lm in landmarks]

    # Zeigefingerspitze für Pan/Tilt-Position
    tip = landmarks[8]
    x_px = int(tip.x * width)
    y_px = int(tip.y * height)

    # Bounding Box über alle Landmarks
    xs = [p[0] for p in landmarks_px]
    ys = [p[1] for p in landmarks_px]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    # --- Rotation der Hand (für Servo-Drehung) ---
    # Vektor vom Handgelenk (0) zum Mittelfinger-Ansatz (9) beschreibt,
    # wie die Hand im Bild gedreht/geneigt ist.
    wrist = landmarks_px[0]
    middle_mcp = landmarks_px[9]
    dx = middle_mcp[0] - wrist[0]
    dy = middle_mcp[1] - wrist[1]

    # Winkel in Grad, 0° = Hand zeigt nach oben, dreht sich mit der Hand mit
    angle_deg = math.degrees(math.atan2(dx, -dy))

    # Zusätzlich: Rotation um die eigene Achse (Roll) über Zeigefinger- (5)
    # und Kleinfinger-Ansatz (17) -> wie "verkantet" die Handfläche ist
    index_mcp = landmarks_px[5]
    pinky_mcp = landmarks_px[17]
    roll_dx = pinky_mcp[0] - index_mcp[0]
    roll_dy = pinky_mcp[1] - index_mcp[1]
    roll_deg = math.degrees(math.atan2(roll_dy, roll_dx))

    return {
        "found": True,
        "x": tip.x,
        "y": tip.y,
        "x_px": x_px,
        "y_px": y_px,
        "bbox": (x_min, y_min, x_max, y_max),
        "landmarks_px": landmarks_px,
        "angle_deg": angle_deg,
        "roll_deg": roll_deg,
    }
