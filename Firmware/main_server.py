import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import cv2
import numpy as np
import threading
import uvicorn

from hand_analyizer import analyze_frame, HAND_CONNECTIONS

load_dotenv()

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

app = FastAPI()

latest_frame = None
latest_result = None
frame_lock = threading.Lock()


@app.post("/upload_frame")
async def upload_frame(request: Request):
    global latest_frame, latest_result
    raw_data = await request.body()

    np_array = np.frombuffer(raw_data, dtype=np.uint8)
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if frame is None:
        return {"found": False}

    result = analyze_frame(frame)

    with frame_lock:
        latest_frame = frame
        latest_result = result

    return result


def draw_hand(frame, result):
    landmarks_px = result["landmarks_px"]

    for start_idx, end_idx in HAND_CONNECTIONS:
        cv2.line(
            frame,
            landmarks_px[start_idx],
            landmarks_px[end_idx],
            color=(0, 255, 0),  # BGR -> Grün
            thickness=2,
        )

    for point in landmarks_px:
        cv2.circle(frame, point, radius=4, color=(0, 0, 255), thickness=-1)

    x_min, y_min, x_max, y_max = result["bbox"]
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color=(255, 0, 0), thickness=2)

    angle_text = f"angle: {result['angle_deg']:.1f} deg"
    roll_text = f"roll: {result['roll_deg']:.1f} deg"
    cv2.putText(frame, angle_text, (x_min, y_min - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, roll_text, (x_min, y_min - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)


def display_loop():
    global latest_frame, latest_result

    while True:
        with frame_lock:
            frame = latest_frame.copy() if latest_frame is not None else None
            result = latest_result

        if frame is not None:
            if result is not None and result.get("found"):
                draw_hand(frame, result)

            cv2.imshow("Empfangener Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    server_thread = threading.Thread(
        target=lambda: uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT),
        daemon=True
    )
    server_thread.start()

    display_loop()
