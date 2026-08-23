# We import the GPIO module
import RPi.GPIO as GPIO
# We import the command sleep from time
from time import sleep

# Stops all warnings from appearing
GPIO.setwarnings(False)

# We name all the pins in BOARD mode
GPIO.setmode(GPIO.BOARD)
# Set outputs for the PWM signals
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# Set up PWM on both pins at 50Hz
unten = GPIO.PWM(15, 50)  # bottom / pan servo
oben = GPIO.PWM(16, 50)   # top / tilt servo

unten.start(0)
oben.start(0)

# Duty cycle reference for typical SG90-style servos:
#   2.5  -> -90 deg (left / down)
#   7.5  ->   0 deg (neutral / center)
#   12.5 -> +90 deg (right / up)
positions = {
    "neutral": 7.5,
    "left":    2.5,
    "right":   12.5,
}


def move(servo, name, duty, hold=1.0):
    print(f"{name} -> {duty} duty cycle")
    servo.ChangeDutyCycle(duty)
    sleep(hold)
    # stop sending pulses in between moves to avoid servo jitter
    servo.ChangeDutyCycle(0)
    sleep(0.3)


try:
    # 1) center both servos first, so you have a known starting point
    print("=== Centering both servos ===")
    move(unten, "unten", positions["neutral"])
    move(oben, "oben", positions["neutral"])
    sleep(1)

    # 2) test "unten" (pan) alone
    print("=== Testing unten (pan) ===")
    move(unten, "unten", positions["left"])
    move(unten, "unten", positions["right"])
    move(unten, "unten", positions["neutral"])
    sleep(1)

    # 3) test "oben" (tilt) alone
    print("=== Testing oben (tilt) ===")
    move(oben, "oben", positions["left"])
    move(oben, "oben", positions["right"])
    move(oben, "oben", positions["neutral"])
    sleep(1)

    # 4) test both together (corner positions)
    print("=== Testing both together ===")
    move(unten, "unten", positions["left"])
    move(oben, "oben", positions["left"])
    sleep(1)

    move(unten, "unten", positions["right"])
    move(oben, "oben", positions["right"])
    sleep(1)

    move(unten, "unten", positions["neutral"])
    move(oben, "oben", positions["neutral"])

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    unten.stop()
    oben.stop()
    GPIO.cleanup()  # Clean up all the ports we've used
    print("Cleaned up GPIO")