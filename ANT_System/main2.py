import os
import time
import datetime
import phsensor
import ph_automation
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import threading

PH_SENSOR = 0
PH_TOPIC = 'sensor/ph'

LIGHT_PIN = 24
LIGHT_ON_HOUR = 8
LIGHT_ON_MIN = 0
LIGHT_OFF_HOUR = 18
LIGHT_OFF_MIN = 5

ph_sensor = phsensor.PHSensor(0, 14)  # phsensor object
ph = ph_sensor.read_ph(PH_SENSOR)

client = mqtt.Client("ANT system")
client.connect("localhost", 1883)

GPIO.setmode(GPIO.BCM)

# method for ph reading and ph balancing
def ph_sensing(pin):
    global ph
    while True:
        ph = ph_sensor.read_ph(pin)
        client.publish(PH_TOPIC, round(ph, 2))
        time.sleep(0.5)

# method for ph balancing
def ph_balance(ph_min, ph_max):
    ph_automation.GPIOSetup_SS()
    while True:
        ph_automation.ph_balancing_ss(ph, ph_min, ph_max)  #internal one minute delay


#method for ec sensing

#method for ec automation

# method for light cycle
def light_cycle():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_PIN, GPIO.OUT, initial = GPIO.LOW)
    while True:
        now = datetime.datetime.now()
        timestamp = now.strftime("%b %d, %Y %I:%M %p")
        #print(timestamp)
        if(now.hour == LIGHT_ON_HOUR and now.minute == LIGHT_ON_MIN):
            if(not GPIO.input(LIGHT_PIN)):
                GPIO.output(LIGHT_PIN,GPIO.HIGH)
            print(f"Light is on at {timestamp}")
        elif(now.hour == LIGHT_OFF_HOUR and now.minute == LIGHT_OFF_MIN):
            if(GPIO.input(LIGHT_PIN)):
                GPIO.output(LIGHT_OFF_HOUR,GPIO.LOW)
            print(f"Light is off at {timestamp}")
    


if __name__ == '__main__':
    try:
        user_calibrate = input("Calibrate ph probe?(Y/N):")
        if user_calibrate == 'Y':
            user_calibrate = input("Manual or Automatic Calibration(A/M):")
            if(user_calibrate=="A"):
                ph_sensor.automatic_ph_calibration(PH_SENSOR)
            else:
                ph_sensor.ph_calibration(PH_SENSOR)
        t1 = threading.Thread(target=ph_sensing, args=(PH_SENSOR,))
        t1.daemon = True
        t2 = threading.Thread(target=light_cycle)
        t2.daemon = True
        t2.start()
        t1.start()
        ph_balance(5.5,7)
    except KeyboardInterrupt:
        GPIO.cleanup()
        os.system("clear") # clear terminal
        print ("\r\nProgram end     ")
        exit()
