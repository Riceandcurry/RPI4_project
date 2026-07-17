import RPi.GPIO as GPIO
import time

# Set up GPIO using the physical pin numbering
GPIO.setmode(GPIO.BOARD)

# Define the pin connected to the IR Sensor's OUT wire (GPIO 23 -> pin 16)
sensor_pin = 16
GPIO.setup(sensor_pin, GPIO.IN)

try:
    print("IR Sensor Active. Press Ctrl+C to exit.")
    
    while True:
        # Check if the signal goes LOW (detects an obstacle)
        if GPIO.input(sensor_pin) == GPIO.LOW:
            print("Object Detected!")
        else:
            print("Path Clear")
        time.sleep(0.5)
        
except KeyboardInterrupt:
    GPIO.cleanup()
