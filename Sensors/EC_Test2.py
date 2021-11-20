import serial
import re
import sys
import os
import string
import time

#open serial port
ser=serial.Serial('/dev/ttyACM0', 115200)

#temp = [0,0,0,0,0]
#EC = [0,0,0,0,0]
counter = 0

while True:
    SensorData = str(ser.readline().decode("utf-8")).split(' ')
    #print(SensorData)

    #temp[counter] = float(SensorData[0])
    #EC[counter] = float(SensorData[1])
    TempAvg = float(SensorData[0])
    ECAvg = float(SensorData[1])

    #TempCount = 0
    #ECCount = 0

    #for i in range(0,5):
    #    TempCount = TempCount + temp[i]
    #    ECCount = ECCount + EC[i]
    
    #TempAvg = TempCount/5
    #ECAvg = ECCount/5
    #print("Temp[]: ", temp, "EC[]: ", EC, "\n")
    print("Temp: ", TempAvg, "EC: ", ECAvg, "\n")

