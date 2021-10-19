import RPi.GPIO as GPIO
import sys
import time

GPIO.setmode(GPIO.BOARD)

PH_UP = 22
PH_DOWN = 24

PH_MIN = 5.5
PH_MAX = 7

def GPIOSetup():
    GPIO.setup(PH_UP, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PH_DOWN, GPIO.OUT, initial = GPIO.LOW)
if __name__ == '__main__':
    try:
        while True:
            #ph sensing from ad da board

            #if ph level is below range
            GPIO.output(PH_UP, GPIO.HIGH)
            #time.sleep(pump duration)
            GPIO.output(PH_UP, GPIO.LOW)

            #if ph level is above range
            GPIO.output(PH_DOWN, GPIO.HIGH)
             #time.sleep(pump duration)
            GPIO.output(PH_DOWN, GPIO.LOW)

            #ph sensing interval
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit('PH balancing ended')
