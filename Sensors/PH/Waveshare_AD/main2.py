import os
import time
import phsensor
import RPi.GPIO as GPIO

ph_sensor = phsensor.PHSensor(0,14) #phsensor object

try:
    user_calibrate = input("Calibrate ph probe?(Y/N):")
    if user_calibrate == 'Y':
        ph_sensor.ph_calibration(0)
    while True:
        ph_sensor.print_all(0) #print voltage and ph value of pin A0
        time.sleep(0.5) #update every 0.5 seconds

except KeyboardInterrupt:
    GPIO.cleanup()
    os.system("clear") # clear terminal
    print ("\r\nProgram end     ")
    exit()
