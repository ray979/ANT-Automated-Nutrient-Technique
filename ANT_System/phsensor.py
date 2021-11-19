import time
import ADS1256
import RPi.GPIO as GPIO
import os.path

#ADC1256 object and initiation
adc = ADS1256.ADS1256()
adc.ADS1256_init()

#millivolt voltages from calibration
PH7_VOLTAGE_MV = 1773
PH4_VOLTAGE_MV = 1937

NUM_OF_SAMPLES = 20

class PHSensor:
    '''
    PH Sensor Class for Grove PI Sensor with Waveshare High Precision AD/DA board

    Args:
        (int) ph_min: minimum ph value ph sensor can read(default = 0)
        (int) ph_max: maximum ph value ph sensor can read(default = 14)
    '''
    def __init__(self, ph_min = 0, ph_max = 14):
        global PH7_VOLTAGE_MV
        global PH4_VOLTAGE_MV
        self.ph_min = ph_min
        self.ph_max = ph_max
        try:
            with open('phcalibrationvalues.txt','r') as file:
                lines = file.readlines()
                PH7_VOLTAGE_MV = float(lines[0].strip("ph7mv="))
                PH4_VOLTAGE_MV = float(lines[1].strip("ph4mv="))
        except:
            print("phcalibrationvalues.txt not found. Default ph calibration values used")

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
        voltages_sum = 0
        ph = 0

        for i in range(NUM_OF_SAMPLES): #read int NUM_OF_SAMPLES of mv voltage samples from AD/DA board 
            voltages_sum += self.read_voltage_mv(pin)

        voltage_mv = voltages_sum / NUM_OF_SAMPLES #average voltages
        ph = 7 + (voltage_mv - PH7_VOLTAGE_MV) * (-3 / (PH4_VOLTAGE_MV - PH7_VOLTAGE_MV)) #pHx = pH1 + (Ex – E1)(pH2 – pH1)/(E2-E1)

        return ph
    
    def ph_calibration(self,pin):
        '''
        Returns average calibration mv voltages for ph7 and ph4

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board 
        '''

        ph_solution = 0
        
        for i in range(2):
            if i == 0:
                ph_solution = 7
                user_input = input(f"Enter 'Y' when ph sensor is in PH {ph_solution} solution:")
            elif i == 1:
                ph_solution = 4
                user_input = input(f"Enter 'Y' when ph sensor is in PH {ph_solution} solution:")

            while user_input != 'Y': 
                user_input = input(f"Enter 'Y' when ph sensor is in PH {ph_solution} solution:")
            
            voltages_sum = 0
            for i in range(NUM_OF_SAMPLES):#read int NUM_OF_SAMPLES of mv voltage samples from AD/DA board
                voltages_sum += self.read_voltage_mv(pin)
            
            print(f"The average mv voltage for PH {ph_solution} is {voltages_sum/NUM_OF_SAMPLES}")

    
    def automatic_ph_calibration(self,pin):
        '''
        Auto calibrate PH sensor reading. Configure calibration text file value.

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board
        '''
        
        ph_solution = 0
        
        for i in range(2):
            if i == 0:
                ph_solution = 7
                user_input = input(f"Enter 'Y' when ph sensor is in PH {ph_solution} solution:")
            elif i == 1:
                ph_solution = 4
                user_input = input(f"Enter 'Y' when ph sensor is in PH {ph_solution} solution:")

            while user_input != 'Y': 
                user_input = input(f"Enter 'Y' when ph sensor is in PH {ph_solution} solution:")
            
            voltages_sum = 0
            for i in range(NUM_OF_SAMPLES):#read int NUM_OF_SAMPLES of mv voltage samples from AD/DA board
                voltages_sum += self.read_voltage_mv(pin)
            
            print(f"The average mv voltage for PH {ph_solution} is {voltages_sum/NUM_OF_SAMPLES}")
            
            if(not os.path.exists('phcalibrationvalues.txt')):
                with open('phcalibrationvalues.txt', 'w') as f:
                    f.write('ph7mv='+ str(round(voltages_sum/NUM_OF_SAMPLES)) + '\n')
                    f.write('ph4mv='+ str(round(voltages_sum/NUM_OF_SAMPLES)) + '\n')
                
                
            with open('phcalibrationvalues.txt', 'r+') as f1:
                lines = f1.readlines()
                with open('phcalibrationvalues.txt', 'w+') as f2:
                    if ph_solution == 7:
                        lines[0] = 'ph7mv='+ str(round(voltages_sum/NUM_OF_SAMPLES)) + '\n'
                    elif ph_solution == 4:
                        lines[1] = 'ph4mv='+ str(round(voltages_sum/NUM_OF_SAMPLES)) + '\n'
                    f2.writelines(lines)


    def print_all(self,pin):
        '''
        Print updating voltage value and ph value on same line

        Args:
            (int) pin: analog signal pin ph sensor module is connected on AD/DA board
        '''
        print("PIN:A%d Voltage:%lf PH:%.2f"%(pin, self.read_voltage(pin),self.read_ph(pin)))
        print("\33[2A")
