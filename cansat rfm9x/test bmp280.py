import time
import busio
import digitalio
import board
import adafruit_bmp280


class Cansat():

    def __init__(self):
        self.temp = 0.0
        self.pressure = 0.0
        self.altitude = 0.0
        
    def sensor(self):
        #sensor
        i2c = busio.I2C(scl=board.GP1,sda=board.GP0)
        self.bme = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)
        # change this to match the location's pressure (hPa) at sea level
        self.bme.sea_level_pressure = 991

    def readTemp(self):
        temperature_offset = -5
        self.temp = str(self.bme.temperature + temperature_offset) #Convert float to str

    def readAltitude(self):
         self.altitude = str(self.bme.altitude) #Convert float to str

    def readPressure(self):
          self.pressure = str(self.bme.pressure) #Convert float to str

    def getTemp(self):
        return str(self.temp)

    def getPressure(self):
        return str(self.pressure)

    def getAltitude(self):
        return str(self.altitude)

   

if __name__ == '__main__':
    mycansat = Cansat()
    mycansat.sensor()
   
    flag = True
    time.sleep(1)
    while flag:
        mycansat.readTemp()
        print(mycansat.getTemp())
        mycansat.readPressure()
        mycansat.readAltitude()