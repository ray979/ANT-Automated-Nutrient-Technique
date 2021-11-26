import os
import time
import datetime
import phsensor
import automation
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import threading

PH_SENSOR = 0

#MQTT Topics
PH_TOPIC = 'sensor/ph'
EC_TOPIC = 'sensor/ec'

LIGHT_PIN = 24
LIGHT_ON_HOUR = 8
LIGHT_ON_MIN = 0
LIGHT_OFF_HOUR = 18
LIGHT_OFF_MIN = 5

ph_sensor = phsensor.PHSensor(0, 14)  # phsensor object
ph = ph_sensor.read_ph(PH_SENSOR)

ec = automation.EC_Reading()

client = mqtt.Client("ANT system")
client.connect("localhost", 1883)

GPIO.setmode(GPIO.BCM)

# method for real time ph reading with interval of 0.5 seconds
def ph_sensing(pin):
    global ph
    while True:
        ph = ph_sensor.read_ph(pin)
        #publish ph reading to MQTT topic 'sensor/ph'
        client.publish(PH_TOPIC, round(ph, 2))
        time.sleep(0.5)

#method for ec sensing
def ec_sensing():
    global ec
    while True:
        ec = automation.EC_Reading()
        #publish ec reading to MQTT topic 'sensor/ec'
        client.publish(EC_TOPIC,round(ec,2))
        time.sleep(0.5)

# method for ph balancing
def ant_automation(ph_min, ph_max):
    automation.GPIOSetup()
    while True:
        automation.EC_balancing(ec, automation.EC_MIN)
        automation.ph_balancing(ph, ph_min, ph_max)
        #one minute automation interval, allow time for solutions to mix
        time.sleep(60)

# method for light cycle
def light_cycle():
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        timestamp = now.strftime("%b %d, %Y %I:%M %p")
        if(get_time_weight(hour,minute) == get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN)):
            if(not GPIO.input(LIGHT_PIN)):
                GPIO.output(LIGHT_PIN,GPIO.HIGH)
            print(f"Light is on at {timestamp}")
        elif(get_time_weight(hour,minute) == get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN)):
            if(GPIO.input(LIGHT_PIN)):
                GPIO.output(LIGHT_OFF_HOUR,GPIO.LOW)
            print(f"Light is off at {timestamp}")

def get_time_weight(hour,minute):
    return hour + (minute / 60)

# method for light at startup
def light_cycle_startup():
    GPIO.setup(LIGHT_PIN, GPIO.OUT, initial = GPIO.LOW)
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    timestamp = now.strftime("%b %d, %Y %I:%M %p")
    if(get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN) > get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN):
        if(get_time_weight(hour,minute) >= get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN) and get_time_weight(hour,minute) < get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN)):
            GPIO.output(LIGHT_PIN,GPIO.HIGH)
        print(f"Light is on at {timestamp}")
    elif((get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN) < get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN)):
        if(get_time_weight(hour,minute) <= get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN) or get_time_weight(hour,minute) > get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN)):
            GPIO.output(LIGHT_PIN,GPIO.HIGH)
        print(f"Light is on at {timestamp}")
    else:
        GPIO.output(LIGHT_PIN,GPIO.LOW)
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
        t2 = threading.Thread(target=ec_sensing)
        t2.daemon = True
        #t3 = threading.Thread(target=light_cycle)
        #t3.daemon = True
        #t3.start()
        t1.start()
        t2.start()
        ant_automation(5.5,7)
    except KeyboardInterrupt:
        GPIO.cleanup()
        os.system("clear") # clear terminal
        print ("\r\nProgram end     ")
        exit()
    except:
        GPIO.cleanup()
        print("Something went wrong")
        print("Program ended early....")
        exit()
