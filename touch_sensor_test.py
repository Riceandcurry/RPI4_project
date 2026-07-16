import RPi.GPIO as GPIO
import signal

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Touch sensor OUT pin connected to GPIO 25 (pin 22)
TOUCH_PIN = 25

count = 0

# Set touch sensor pin a input
GPIO.setup(TOUCH_PIN, GPIO.IN)

def touch_detected(channel):
    global count
    count += 1
    print("Touch detected! Count:", count)

# Detect rising signal: from Low to HIGH
GPIO.add_event_detect(
    TOUCH_PIN,
    GPIO.RISING,
    callback=touch_detected,
    bouncetime=300
)

print("Touch sensor test started...")
print("Touch the sensor to see the output.")
print("Press Ctrl + C to stop.\n")

try:
    signal.pause() # keeps proram running without printing repeatedly
        
except KeyboardInterrrupt:
    print("\nTest stopped by user.")
    
finally:
    GPIO.cleanup()
