import cv2
from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()
time.sleep(1)  # kurze Wartezeit, damit Belichtung sich einpendelt

while True:
    img = picam2.capture_array()  # liefert direkt ein numpy-Array (OpenCV-kompatibel)
    cv2.imshow("CamOutput", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Fenster schließt sich bei Taste 'q'
        break

picam2.stop()
cv2.destroyAllWindows()