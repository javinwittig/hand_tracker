import subprocess
import threading
from time import sleep

import cv2
import numpy as np
import requests
import RPi.GPIO as GPIO

WIDTH, HEIGHT = 640, 480
FRAME_SIZE = int(WIDTH * HEIGHT * 1.5)

SERVER_URL = "http://192.168.178.88:8000/upload_frame"

# Gleiches Setup wie im Servo-Testskript: BOARD-Pins 15 & 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

oben = GPIO.PWM(15, 50)  # bottom / pan servo  -> gesteuert mit angle_deg
unten = GPIO.PWM(16, 50)   # top / tilt servo    -> gesteuert mit roll_deg

unten.start(0)
oben.start(0)

# Duty cycle reference for typical SG90-style servos (wie im Testskript):
#   2.5  -> -90 deg
#   7.5  ->   0 deg (neutral)
#   12.5 -> +90 deg
DUTY_MIN = 2.5
DUTY_NEUTRAL = 7.5
DUTY_MAX = 12.5

# Eingabe-Winkelbereich, den angle_deg / roll_deg vom Server tatsächlich
# liefern. Erstmal die geprinteten Werte beim Handbewegen beobachten und
# dann hier den echten Bereich eintragen - sonst nutzt der Servo nicht
# seinen vollen Bewegungsbereich oder schlägt zu früh am Anschlag an.
PAN_ANGLE_RANGE = (-90, 90)    # für angle_deg (unten)
TILT_ANGLE_RANGE = (-90, 90)   # für roll_deg (oben)

# Wie schnell der Servo dem Zielwert hinterherfährt (0 < x <= 1).
# Kleiner = weicher/langsamer, 1.0 = sofort, keine Glättung.
SMOOTHING = 0.3

lock = threading.Lock()
target_pan_duty = DUTY_NEUTRAL
target_tilt_duty = DUTY_NEUTRAL


def clamp(value, low, high):
    return max(low, min(high, value))


def angle_to_duty(angle_deg, angle_range):
    """Rechnet einen Winkel (Grad) linear in eine Servo-Duty-Cycle um."""
    lo, hi = angle_range
    angle_deg = clamp(angle_deg, lo, hi)
    ratio = (angle_deg - lo) / (hi - lo)
    return DUTY_MIN + ratio * (DUTY_MAX - DUTY_MIN)


def servo_loop():
    """Läuft im eigenen Thread und bewegt die Servos weich in Richtung
    Zielwert - unabhängig vom Netzwerk-Roundtrip. Glättet das Jitter aus
    der Handerkennung, statt jeden einzelnen (verrauschten) Frame-Wert
    sofort 1:1 auf den Servo zu geben. Anders als im Testskript wird die
    Duty Cycle NICHT zwischen den Updates auf 0 gesetzt - beim Tracking
    soll der Servo durchgehend gehalten/nachgeführt werden, nicht nur
    kurz anfahren und dann lose hängen."""
    current_pan = DUTY_NEUTRAL
    current_tilt = DUTY_NEUTRAL

    while True:
        with lock:
            t_pan = target_pan_duty
            t_tilt = target_tilt_duty

        current_pan += (t_pan - current_pan) * SMOOTHING
        current_tilt += (t_tilt - current_tilt) * SMOOTHING

        unten.ChangeDutyCycle(current_pan)
        oben.ChangeDutyCycle(current_tilt)

        sleep(0.02)  # ~50 Hz


def generate_frames():
    global target_pan_duty, target_tilt_duty

    cmd = [
        "rpicam-vid", "-t", "0",
        "--width", str(WIDTH), "--height", str(HEIGHT),
        "--framerate", "15", "--codec", "yuv420",
        "--rotation", "180", "-o", "-", "-n"
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**7)

    try:
        while True:
            raw_data = process.stdout.read(FRAME_SIZE)
            if len(raw_data) != FRAME_SIZE:
                print("error reading frame")
                break

            yuv = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(HEIGHT * 1.5), WIDTH))
            frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)
            frame = cv2.flip(frame, 1)

            if frame.mean() < 25.0:
                print("frame too dark - check lighting / lens")
                continue

            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 65])
            frame_bytes = buffer.tobytes()

            try:
                answer = requests.post(SERVER_URL, data=frame_bytes, timeout=1)
                result = answer.json()
            except (requests.exceptions.RequestException, ValueError) as e:
                print(f"Senden fehlgeschlagen: {e}")
                continue

            if result.get("found"):
                pan_duty = angle_to_duty(result["angle_deg"], PAN_ANGLE_RANGE)
                tilt_duty = angle_to_duty(result["roll_deg"], TILT_ANGLE_RANGE)

                print(f"angle_deg={result['angle_deg']:.1f} -> pan_duty={pan_duty:.2f} | "
                      f"roll_deg={result['roll_deg']:.1f} -> tilt_duty={tilt_duty:.2f}")

                with lock:
                    target_pan_duty = pan_duty
                    target_tilt_duty = tilt_duty
    finally:
        process.terminate()
        unten.stop()
        oben.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    print("Starting ...")
    threading.Thread(target=servo_loop, daemon=True).start()
    generate_frames()