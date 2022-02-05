import time
import ADS1256
import RPi.GPIO as GPIO
import os.path
import sys
from w1thermsensor import W1ThermSensor 


#ADC1256 object and initiation
adc = ADS1256.ADS1256()
adc.ADS1256_init()

#temp sensor object
temp_sensor = W1ThermSensor()

_kvalue                 = 1.0
_kvalueLow              = 1.0
_kvalueHigh             = 1.0
_cmdReceivedBufferIndex = 0
_voltage                = 0.0
_temperature            = 25.0

class ECSensor:
    def begin(self):
        global _kvalueLow
        global _kvalueHigh
        try:
          with open('ecdata.txt','r') as f:
              kvalueLowLine  = f.readline()
              kvalueLowLine  = kvalueLowLine.strip('kvalueLow=')
              _kvalueLow     = float(kvalueLowLine)
              kvalueHighLine = f.readline()
              kvalueHighLine = kvalueHighLine.strip('kvalueHigh=')
              _kvalueHigh    = float(kvalueHighLine)
        except :
          print("ecdata.txt ERROR ! Please run DFRobot_EC_Reset")
          sys.exit(1)
    
    def read_voltage(self,pin):
        '''
        Read voltage value from ec sensor through AD/DA board

        Args:
            (int) pin: analog signal pin ec sensor module is connected on AD/DA board
        '''
        adc_value = adc.ADS1256_GetAll()
        voltage = adc_value[pin] * 5.0/ 0x7fffff #voltage - adc data * supply voltage/0x7fffff because 24bit ADC
        return voltage

    def read_voltage_mv(self,pin):
        '''
        Read millivolt voltage value from ec sensor through AD/DA board

        Args:
            (int) pin: analog signal pin ec sensor module is connected on AD/DA board
        '''
        return self.read_voltage(pin) * 1000

    def readEC(self,pin):
        voltage = self.read_voltage(pin)
        temperature = temp_sensor.get_temperature()
        global _kvalueLow
        global _kvalueHigh
        global _kvalue
        rawEC = 1000*voltage/820.0/200.0
        valueTemp = rawEC * _kvalue
        if(valueTemp > 2.5):
            _kvalue = _kvalueHigh
        elif(valueTemp < 2.0):
          _kvalue = _kvalueLow
        value = rawEC * _kvalue
        value = (value / (1.0+0.0185*(temperature-25.0))) * 1000
        return value
