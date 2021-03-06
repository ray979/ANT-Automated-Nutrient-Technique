import os
import time
import datetime
import phsensor
import ecsensor
import automation
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import threading
import requests
import json

#PH and EC sensor ADC Pins
PH_SENSOR = 0
EC_SENSOR = 1

PH_MIN = 5.5
PH_MAX = 7

ph_sensor = phsensor.PHSensor(0, 14)  # phsensor object
ph = ph_sensor.read_ph(PH_SENSOR)


#ec = automation.EC_Reading()
ec_sensor = ecsensor.ECSensor() #ec sensor object
ec = ec_sensor.readEC(1)

#MQTT Topics
PH_TOPIC = 'sensor/ph'
EC_TOPIC = 'sensor/ec'
AUTOMATION_TOPIC = 'automation/pumps'

#Last saved to database
LAST_SAVED_TO_DATABASE = None

#MQTT subscribe topics for settings
settings_topic =[
    ('/PHMINSET',0),
    ('/PHMAXSET',0),
    ('/ECMINSET',0),
    ('/LIGHSTARTSET',0),
    ('/LIGHTENDSET',0)
]

#Light Cycle Settings
LIGHT_PIN = 5
LIGHT_ON_HOUR = 8
LIGHT_ON_MIN = 0
LIGHT_OFF_HOUR = 18
LIGHT_OFF_MIN = 0

#thread lock
lock = threading.Lock()

def on_message(client, userdata, message):
    '''
    MQTT On message method callback. Changes setting values based on mqtt message to topic.
    '''
    global PH_MIN
    global PH_MAX
    global EC_MIN
    global LIGHT_ON_HOUR
    global LIGHT_OFF_HOUR

    try:
        if(message.topic == settings_topic[0][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            PH_MIN = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'PH Min value changed {PH_MIN}')
            lock.release()
        elif(message.topic == settings_topic[1][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            PH_MAX = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'PH Max value changed {PH_MAX}')
            lock.release()
        elif(message.topic == settings_topic[2][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            EC_MIN = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'EC Min value changed {EC_MIN}')
            lock.release()
        elif(message.topic == settings_topic[3][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            LIGHT_ON_HOUR = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'LIGHT Start Hour value changed {LIGHT_ON_HOUR}')
            lock.release()
        elif(message.topic == settings_topic[4][0]):
            print(f'The message is {str(message.payload.decode("utf-8"))}')
            lock.acquire()
            LIGHT_OFF_HOUR = round(float(str(message.payload.decode("utf-8"))),2)
            print(f'LIGHT Off Hour value changed {LIGHT_OFF_HOUR}')
            lock.release()
    except ValueError as e:
        print("Cannot convert string to float")


#MQTT Client connect and topic subscriptions
client = mqtt.Client("ANT system")
client.connect("localhost", 1883)
client.on_message = on_message
client.subscribe(settings_topic)
client.loop_start()

#method for saving sensordata into database
def save_sensordata_to_database(ph,ec):
    global LAST_SAVED_TO_DATABASE
    
    #data to be saved
    new_sensor_data = {
        "ph":ph,
        "ec":ec
    }
    
    try:
        # Make a post request to fastapi endpoint for storing sensor data, post data should be in json format
        request = requests.post("http://127.0.0.1:8000/sensordata", json.dumps(newsensordata,indent=3))
        
        if(request.status_code == 200): #only update last saved when status code is 200
            LAST_SAVED_TO_DATABASE = datetime.datetime.now()
    except Exception as e:
        print("Could not save sensor data into database")

# method for real time ph reading with interval of 0.5 seconds
def ph_sensing(pin):
    global ph
    while True:
        lock.acquire()
        ph = ph_sensor.read_ph(pin) #read ph
        lock.release()
        #publish ph reading to MQTT topic 'sensor/ph'
        client.publish(PH_TOPIC, round(ph, 2))
        time.sleep(0.5)

#method for ec sensing
def ec_sensing(pin):
    global ec
    while True:
        lock.acquire()
        ec = ec_sensor.readEC(pin) #read ec
        lock.release()
        #publish ec reading to MQTT topic 'sensor/ec'
        client.publish(EC_TOPIC,ec)
        time.sleep(0.5)

# method for ph balancing
def ant_automation(ph_min, ph_max, ec_min):
    #Saving to database for first time
    if(LAST_SAVED_TO_DATABASE is None):
        save_sensordata_to_database(ph,ec)
    
    while True:
        #Save sensor readings to database before every automation cycle
        if(LAST_SAVED_TO_DATABASE is not None):
            if((LAST_SAVED_TO_DATABASE + datetime.timedelta(minutes = 30)) <= datetime.datetime.now()):
                save_sensordata_to_database(ph,ec)
        
        #EC automation        
        ec_auto_code = automation.EC_balancing(ec, automation.EC_MIN)
        if(ec_auto_code == 1): #ec dosing pumps were turned on
            client.publish(AUTOMATION_TOPIC,"Nutrient A and B dosed")
            time.sleep(1200) #wait 20 min for nutrients to mix
        
        #PH automation
        ph_auto_code = automation.ph_balancing(ph, ph_min, ph_max)
        if(ph_auto_code == 1): #PH up pump turned on
            client.publish(AUTOMATION_TOPIC,"PH UP dosed")
            time.sleep(900) #wait 15 min for ph adjuster to mix
        elif(ph_auto_code == 2): #PH down pump turned on
            client.publish(AUTOMATION_TOPIC,"PH DOWN dosed")
            time.sleep(900)
        
        #ten minute automation interval
        time.sleep(600)

# method for light cycle
def light_cycle():
    #Intial startup of light cycle
    light_cycle_startup()
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        timestamp = now.strftime("%b %d, %Y %I:%M %p")
        
        #Turn on light if current time is at light on time and turn off lights if current time is at light off time
        if(get_time_weight(hour,minute) == get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN)):
            if(not GPIO.input(LIGHT_PIN)):
                GPIO.output(LIGHT_PIN,GPIO.HIGH)
                print(f"Light is on at {timestamp}")
                time.sleep(60-second+1)
        elif(get_time_weight(hour,minute) == get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN)):
            if(GPIO.input(LIGHT_PIN)):
                GPIO.output(LIGHT_PIN,GPIO.LOW)
                print(f"Light is off at {timestamp}")
                time.sleep(60-second+1)

# method for turning time with hour and minutes to a weighted value
def get_time_weight(hour,minute):
    return hour + (minute / 60)

# method for light at startup, determine initial light state
def light_cycle_startup():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    timestamp = now.strftime("%b %d, %Y %I:%M %p")
    
    #if light off time is greater than light on time
    if(get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN) > get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN)):
        #if current time is between turn on time and turn off time, turn on light
        if(get_time_weight(hour,minute) >= get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN) and get_time_weight(hour,minute) < get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN)):
            GPIO.output(LIGHT_PIN,GPIO.HIGH)
            print(f"Light is on at {timestamp}")
        else:
            GPIO.output(LIGHT_PIN,GPIO.LOW)
            print(f"Light is off at {timestamp}")
    elif(get_time_weight(LIGHT_OFF_HOUR,LIGHT_OFF_MIN) < get_time_weight(LIGHT_ON_HOUR,LIGHT_ON_MIN)): #if light off time is less than light on time
        #if current time is between turn on time and turn off time, turn on light
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

        #GPIO Pin setup
        GPIO.setmode(GPIO.BCM)
        automation.GPIOSetup()
        GPIO.setup(LIGHT_PIN, GPIO.OUT, initial = GPIO.LOW)

        t1 = threading.Thread(target=ph_sensing, args=(PH_SENSOR,))
        t1.daemon = True
        t2 = threading.Thread(target=ec_sensing, args=(EC_SENSOR,))
        t2.daemon = True
        t3 = threading.Thread(target=light_cycle)
        t3.daemon = True
        t1.start()
        t2.start()
        t3.start()
        ant_automation(5.5,7, 17.50)
    except KeyboardInterrupt:
        GPIO.output(5,GPIO.LOW)
        client.loop_stop()
        os.system("clear") # clear terminal
        print ("\r\nProgram end     ")
        GPIO.cleanup()
        exit()
    except Exception as e:
        GPIO.cleanup()
        print("Something went wrong")
        print(e)
        print("Program ended early....")
        exit()
