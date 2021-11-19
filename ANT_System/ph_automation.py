import RPi.GPIO as GPIO
import phsensor
import sys
import time

PH_SENSOR_PIN = 0

PH_UP = 25
PH_DOWN = 5

PH_MIN = 5.5
PH_MAX = 7

def GPIOSetup():
    GPIO.setup(PH_UP, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(PH_DOWN, GPIO.OUT, initial = GPIO.HIGH)
    
def GPIOSetup_SS():
    GPIO.setup(PH_UP, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PH_DOWN, GPIO.OUT, initial = GPIO.LOW)

def ph_balancing(ph_reading,ph_min,ph_max):
    #ph sensing from ad da board
    ph = round(ph_reading,1)

    #if ph level is below range
    if ph < ph_min:
        #turn on PH up pump
        GPIO.output(PH_UP, GPIO.LOW)
        print(f"PH UP pump on at PH:{ph}")
        #time.sleep(pump duration)
        time.sleep(1)
        #turn off PH up pump
        GPIO.output(PH_UP, GPIO.HIGH)
        print("PH UP pump off")

    #if ph level is above range
    if ph > ph_max:
        #turn on PH down pump
        GPIO.output(PH_DOWN, GPIO.LOW)
        print(f"PH DOWN pump on at PH:{ph}")
        #time.sleep(pump duration)
        time.sleep(1)
        #turn off PH down pump
        GPIO.output(PH_DOWN, GPIO.HIGH)
        print("PH DOWN pump off")

    #ph sensing interval
    time.sleep(60)
        
def ph_balancing_ss(ph_reading,ph_min,ph_max):
    #ph sensing from ad da board
    ph = round(ph_reading,1)

    #if ph level is below range
    if ph < ph_min:
        #turn on PH up pump
        GPIO.output(PH_UP, GPIO.HIGH)
        print(f"PH UP pump on at PH:{ph}")
        #time.sleep(pump duration)
        time.sleep(1)
        #turn off PH up pump
        GPIO.output(PH_UP, GPIO.LOW)
        print("PH UP pump off")

    #if ph level is above range
    if ph > ph_max:
        #turn on PH down pump
        GPIO.output(PH_DOWN, GPIO.HIGH)
        print(f"PH DOWN pump on at PH:{ph}")
        #time.sleep(pump duration)
        time.sleep(1)
        #turn off PH down pump
        GPIO.output(PH_DOWN, GPIO.LOW)
        print("PH DOWN pump off")

    #ph sensing interval
    time.sleep(60)
            

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        GPIOSetup_SS()
        ph_sensor = phsensor.PHSensor(0,14) #phsensor object
        while True:
            ph_balancing_ss(ph_sensor.read_ph(PH_SENSOR_PIN),PH_MIN,PH_MAX)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit('PH balancing ended')

