import RPi.GPIO as GPIO
import time

EC_A = 30
EC_B = 35

def EC_balancing(EC_reading,EC_min):
    #if EC level is below range, turn on pump
    if EC_reading < EC_min:
        #turn on EC pumps
        GPIO.output(EC_A, GPIO.LOW)
        print("EC: ", EC_reading, "\nStarting pump for Solution A")
        #time.sleep(pump duration)
        time.sleep(1)
        #turn off pump
        GPIO.output(EC_A, GPIO.HIGH)
        print("Solution A pump off")

        #then Solution B
        GPIO.output(EC_B, GPIO.LOW)
        print("Starting pump for Solution A")
        #time.sleep(pump duration)
        time.sleep(2)
        #turn off pump
        GPIO.output(EC_B, GPIO.HIGH)
        print("Solution B pump off")
