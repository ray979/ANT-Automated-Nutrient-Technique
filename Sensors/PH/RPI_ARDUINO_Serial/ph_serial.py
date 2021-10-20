import serial
import re
import sys
import os

#opening serial port
ser=serial.Serial('/dev/ttyACM0', 9600)
#Here /dev/ttyACM0 used
#Find the right usb interface for your device using 'ls /dev/tty*'

while True:
    try:
        serialdata = str(ser.readline()).split(' ') #split line read by space

        if (len(serialdata) > 1):

            pattern = re.compile(r"[\d]+[.]?[\d]+") #real expression: Find numerical value in form "xx.xx"

            try:
                voltage_value = float(pattern.search(serialdata[0]).group()) #apply real expression to serial data
                ph_value = float(pattern.search(serialdata[1]).group())
                os.system('clear')
                print(f'Voltage:{voltage_value} PH:{ph_value}')
            except AttributeError as e: #if real expression return None
                print(e)

    except KeyboardInterrupt:
        print('End of ph sensing') 
        sys.exit()#exit program
