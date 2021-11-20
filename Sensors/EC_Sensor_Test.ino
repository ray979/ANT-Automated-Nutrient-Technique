#include <DS18B20.h>
#include "DFRobot_EC.h"
#include <EEPROM.h>
#include <DallasTemperature.h>

#define EC_PIN A1
#define Temp_Sensor 4

float voltage,ecValue,temperature = 25;
float avgEC;
float avgTemp;
float ecArray[5];
float tempArray[5];

DFRobot_EC ec;
OneWire oneWire(Temp_Sensor); 
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);  
  ec.begin();
  sensors.begin();
}

void loop() 
{
    static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U)  //time interval: 1s
    {
      timepoint = millis();
      
      for(int i = 0; i<5; i++){
        voltage = analogRead(EC_PIN)/1024.0*5000;   // read the voltage
        //temperature = 25;                           //Temporary value until temp sensor added
        temperature = readTemperature();          // read your temperature sensor to execute temperature compensation
        ecValue =  ec.readEC(voltage,temperature);  // convert voltage to EC with temperature compensation
        ecArray[i] = ecValue;
        tempArray[i] = temperature;
        //Serial.print("ecValue: ");
        //Serial.print(ecValue, 2);
        //Serial.print("temp: ");
        //Serial.print(temperature, 1);
        //delay(1000); 
        //Serial.print("temperature:");
        //Serial.print(temperature,1);
        //Serial.print(" ");
        //Serial.print("^C  EC:");
        //Serial.print(ecValue,2);
        //Serial.print("\n");
        //Serial.println("ms/cm");

      }

      //Calculate average EC and temp
      //count = 0;
      float ecSum = 0;
      float tempSum = 0;
      for(int i = 0; i<5; i++){
        ecSum = ecSum + ecArray[i];
        tempSum = tempSum + tempArray[i];          
      }
      avgEC = ecSum/5;
      avgTemp = tempSum/5;

      //Serial.print("avgTemp: ");
      Serial.print(avgTemp,1);
      Serial.print(" ");
      //Serial.print("avgEC: ");
      Serial.print(avgEC,2);
      Serial.print("\n");

      delay(1000);
    }
    ec.calibration(voltage,temperature);          // calibration process by Serail CMD
}

float readTemperature() {
  //Serial.print(" Requesting temperatures..."); 
  sensors.requestTemperatures(); // Send the command to get temperature readings 
  //Serial.println("DONE"); 
/********************************************************************/
  //Serial.print("Temperature is: "); 
  temperature = (sensors.getTempCByIndex(0)); // Why "byIndex"?  
   // You can have more than one DS18B20 on the same bus.  
   // 0 refers to the first IC on the wire 
  //delay(1000);
  return temperature;
}

/*
#define EC_PIN A1
#define 

float voltage,ecValue,temperature = 25;
DFRobot_EC ec;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);  
  ec.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  static unsigned long timepoint = millis();
    if(millis()-timepoint>1000U)  //time interval: 1s
    {
      timepoint = millis();
      voltage = analogRead(EC_PIN)/1024.0*5000;   // read the voltage
      temperature = 25;                           //Temporary value until temp sensor added
      //temperature = readTemperature();          // read your temperature sensor to execute temperature compensation
      ecValue =  ec.readEC(voltage,temperature);  // convert voltage to EC with temperature compensation
      //Serial.print("temperature:");
      Serial.print(temperature,1);
      //Serial.print("^C  EC:");
      Serial.print(" ");
      Serial.print(ecValue,2);
      Serial.print("\n");
      //Serial.println("ms/cm");
    }
    ec.calibration(voltage,temperature);          // calibration process by Serail CMD

}

float readTemperature() {
  //Serial.print(" Requesting temperatures..."); 
  sensors.requestTemperatures(); // Send the command to get temperature readings 
  //Serial.println("DONE"); 
  //Serial.print("Temperature is: "); 
  temperature = (sensors.getTempCByIndex(0)); // Why "byIndex"?  
   // You can have more than one DS18B20 on the same bus.  
   // 0 refers to the first IC on the wire 
  delay(1000);
  return temperature;
}
*/
