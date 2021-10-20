import time
import ADS1256
import RPi.GPIO as GPIO

#ADC1256 object and initiation
adc = ADS1256.ADS1256()
adc.ADS1256_init()

#millivolt voltages from calibration
PH7_VOLTAGE_MV = 1780
PH4_VOLTAGE_MV = 1940

class PHSensor:
    '''
    PH Sensor Class for Grove PI Sensor with Waveshare High Precision AD/DA board

    Args:
        (int) ph_min: minimum ph value ph sensor can read(default = 0)
        (int) ph_max: maximum ph value ph sensor can read(default = 14)
    '''
    def __init__(self, ph_min = 0, ph_max = 14):
        self.ph_min = ph_min
        self.ph_max = ph_max

    def read_voltage(self,pin):
        '''
        Read voltage value from ph sensor through AD/DA board

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board
        '''
        adc_value = adc.ADS1256_GetAll()
        voltage = adc_value[pin] * 5.0/ 0x7fffff #voltage - adc data * supply voltage/0x7fffff because 24bit ADC
        return voltage

    def read_voltage_mv(self,pin):
        '''
        Read millivolt voltage value from ph sensor through AD/DA board

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board
        '''
        return self.read_voltage(pin) * 1000

    def read_ph(self, pin):
        '''
        Read ph value from ph sensor through AD/DA board

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board
        '''
        adc_value = adc.ADS1256_GetAll() #get list of adc values from all adc pins
        voltage_mv = (adc_value[pin] * 1000 * 5.0)/0x7fffff
        ph = 7 + (voltage_mv - PH7_VOLTAGE_MV) * (-3 / (PH4_VOLTAGE_MV - PH7_VOLTAGE_MV)) #pHx = pH1 + (Ex – E1)(pH2 – pH1)/(E2-E1)
        return ph

    def print_all(self,pin):
        '''
        Print updating voltage value and ph value on same line

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board
        '''
        print("PIN:A%d Voltage:%lf PH:%.2f"%(pin, self.read_voltage(pin),self.read_ph(pin)))
        print("\33[2A")
