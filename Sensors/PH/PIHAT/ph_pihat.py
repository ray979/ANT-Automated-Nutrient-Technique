from grove.adc_8chan_12bit import Pi_hat_adc
import time
import sys

#ADC object
adc = Pi_hat_adc()

while True:
    try:
        voltage = (adc.get_nchan_adc_raw_data(2) * 3.3)/4096 #get voltage - ADC data * supply voltage(3.3V) / 4096 since 12bit ADC
        voltage_mv = voltage * 1000
        ph = 7 + (voltage_mv - 2415) * -0.024 #pHx = pH1 + (Ex – E1)(pH2 – pH1)/(E2-E1)
        print(f"Voltage:%.2f PH:%.2f"%(voltage,ph))
        #print ("\33[2A") #Move cursor up 2 line
        time.sleep(1)

    except KeyboardInterrupt:
        print("Ph sensing ended")
        sys.exit()