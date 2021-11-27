import RPi.GPIO as GPIO
import time
import serial
import re
import sys
import os
import string

EC_A = 30
EC_B = 35
EC_MIN = 1.2

def GPIOSetup():
    GPIO.setup(EC_A, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(EC_B, GPIO.OUT, initial = GPIO.HIGH)
    
def GPIOSetup_SS():
    GPIO.setup(EC_A, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(EC_B, GPIO.OUT, initial = GPIO.LOW)

def EC_balancing(EC_reading,EC_min):
    #if EC level is below range, turn on pump
    EC_reading =  EC_Reading()
    if EC_reading < EC_min:
        #turn on EC pumps
        GPIO.output(EC_A, GPIO.LOW)
        print("EC: ", EC_reading, "\nStarting pump for Solution A")
        time.sleep(1)
        GPIO.output(EC_A, GPIO.HIGH)
        print("Solution A pump off")

        #then Solution B
        GPIO.output(EC_B, GPIO.LOW)
        print("Starting pump for Solution A")
        time.sleep(2)
        GPIO.output(EC_B, GPIO.HIGH)
        print("Solution B pump off")

def EC_Reading():
    #open serial port
    ser=serial.Serial('/dev/ttyACM0', 115200)

    SensorData = str(ser.readline().decode("utf-8")).split(' ')

    TempAvg = float(SensorData[0])
    ECAvg = float(SensorData[1])

    print("Temp: ", TempAvg, "EC: ", ECAvg, "\n")
    return ECAvg

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        GPIOSetup_SS()
        while True:
            EC_balancing(EC_Reading, EC_MIN)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit('EC balancing ended')
