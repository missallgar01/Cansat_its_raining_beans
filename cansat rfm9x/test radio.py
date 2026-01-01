import time
import busio
import digitalio
import board
import adafruit_rfm9x
import adafruit_bmp280
from adafruit_motor import motor
import pwmio
import analogio


class Cansat():

    def __init__(self):
        self.temp = 0
       

    def sensor(self):
        #sensor
        i2c = busio.I2C(scl=board.GP1,sda=board.GP0)
        self.bme = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=0x76)
        # change this to match the location's pressure (hPa) at sea level
        self.bme.sea_level_pressure = 991

    def radio(self):
        # Radio
        spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
        cs = digitalio.DigitalInOut(board.GP6)
        reset = digitalio.DigitalInOut(board.GP7)
        self.rfm9x = adafruit_rfm9x.RFM9x(spi,cs,reset,433.0,baudrate=921600)

    def send(self,message):
        self.rfm9x.send(message)

    def readTemp(self):
        temperature_offset = -5
        self.temp = str(self.bme.temperature + temperature_offset) #Convert float to str

    def getTemp(self):
        return str(self.temp)

    
    def sendTemp(self):
        data = "1" + str(self.temp)
        packet = bytearray(data)
        print(packet)
        self.send(packet)

    def sendData(self):
        
        self.readTemp()
        self.sendTemp()
       
        
if __name__ == '__main__':
    mycansat = Cansat()
    mycansat.radio()
    mycansat.sensor()

    while True:
    
        mycansat.sendData()
        time.sleep(2)
      