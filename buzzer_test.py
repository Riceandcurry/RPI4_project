import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# GPIO 24 (pin 18)
BUZZER_PIN = 24

GPIO.setup(BUZZER_PIN, GPIO.OUT)

print("Buzzer test started.")

try:
    print("Buzzer ON")
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    
    print("Buzzer OFF")
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    print("Buzzer test completed.")
    
except KeyboardInterrupt:
    print("Test stopped by user.")
    
finally:
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.cleanup()
    
