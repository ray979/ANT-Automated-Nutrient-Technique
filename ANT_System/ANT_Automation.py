import RPi.GPIO as GPIO
import phsensor
import sys
import time
import os
import string
import re
import serial

PH_SENSOR_PIN = 0

PH_UP = 7
PH_DOWN = 18

PH_MIN = 5.5
PH_MAX = 7

EC_A = 30
EC_B = 35
EC_MIN = 17.50


def GPIOSetup():
    GPIO.setup(PH_UP, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(PH_DOWN, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(EC_A, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(EC_B, GPIO.OUT, initial = GPIO.HIGH)
    
def GPIOSetup_SS():
    GPIO.setup(PH_UP, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PH_DOWN, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(EC_A, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(EC_B, GPIO.OUT, initial = GPIO.LOW)


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
            
def EC_Reading():
    #open serial port
    ser=serial.Serial('/dev/ttyACM0', 115200)

    SensorData = str(ser.readline().decode("utf-8")).split(' ')

    TempAvg = float(SensorData[0])
    ECAvg = float(SensorData[1])

    print("Temp: ", TempAvg, "EC: ", ECAvg, "\n")
    return ECAvg

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

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        GPIOSetup_SS()
        ph_sensor = phsensor.PHSensor(0,14) #phsensor object
        while True:
            ph_balancing_ss(ph_sensor.read_ph(PH_SENSOR_PIN),PH_MIN,PH_MAX)
            EC_balancing(EC_Reading(), EC_MIN)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit('PH balancing ended')