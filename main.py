from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()
picam2.capture_file("/home/javin/tracker/img.jpg")
picam2.stop()
print("Done.")