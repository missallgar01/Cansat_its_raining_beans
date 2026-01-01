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
        self.pressure = 0
        self.altitude = 0
        self.light = False
        self.datastr = ""
        self.pumpStatus = False
        self.cansat = False

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
    
    def getPumpStatus(self):
        return self.pumpStatus
    
    def getCansat(self):
        return self.cansat
    
    # You will usually have to add an offset to account for the temperature of
    # the sensor. This is usually around 5 degrees but varies by use. Use a
    # separate temperature sensor to calibrate this one.
    def sendTemp(self):
        data = "1" + str(self.temp)
        packet = bytearray(data)
        print(packet)
        self.send(packet)

    def sendPressure(self):

        data = "2" + str(self.pressure)
        packet = bytearray(data)
        print(packet)
        self.send(packet)

    def sendAltitude(self):
        data = "3" + str(self.altitude)
        packet = bytearray(data)
        print(packet)
        self.send(packet)
        
    def sendPumpStatus(self):
        data = "4" + str(self.pumpStatus)
        packet = bytearray(data)
        print(packet)
        self.send(packet)

    def configurePump(self):
        PWM_PIN_A = board.GP19 #AIN2
        PWM_PIN_B = board.GP18 #AIN1
        self.pwm_a = pwmio.PWMOut(PWM_PIN_A,frequency = 50)
        self.pwm_b = pwmio.PWMOut(PWM_PIN_B,frequency = 50)
        self.motor1 = motor.DCMotor(self.pwm_a,self.pwm_b)
        
    def startPump(self):
        self.motor1.throttle = 1
        print("throttle:",self.motor1.throttle)
        
    def stopPump(self):
        self.motor1.throttle = 0
        print("DC motor stop")
    
    def try_read(self):
        return self.rfm9x.receive(timeout=5.0)
    
    def receive(self):
        data = self.try_read()
        print("Receiving data",data)
        packet = [] #to store data from bytearray into a list
        self.datastr = ""
        if data is not None:

            for value in data: #append arraybytes data into a list
                packet.append(value)

            for num in packet:
                self.datastr = self.datastr + chr(num)
            if self.datastr[0] == "7":
                self.cansat = True
            if self.datastr[0] == "8":
                self.cansat = False
            if self.datastr[0] == "5":  # turn on pump
                self.pumpStatus = True
            if self.datastr[0] == "6": # turn off pump
                self.pumpStatus = False
    
    def configureLight(self):
        
        self.photoresistor = analogio.AnalogIn(board.GP26)
       
    
    def checkLight(self):
        lightLevel = self.photoresistor.value
        lightLevel = round(lightLevel/65535*100,2)
        print(lightLevel)
        
        if lightLevel < 90:
            print("Light!")
            self.light = True
        else:
            print("Dark!")
            self.light = False
        
        return self.light
        
    def sendData(self):
        
        self.readTemp()
        self.sendTemp()
        self.readPressure()
        self.sendPressure()
        self.readAltitude()
        self.sendAltitude()
        self.sendPumpStatus()
        
if __name__ == '__main__':
    mycansat = Cansat()
    mycansat.radio()
    mycansat.sensor()
    mycansat.configureLight()
    mycansat.configurePump()
    
    def checkPump(mycansat):
        if mycansat.getPumpStatus():
            mycansat.startPump()
        if not mycansat.getPumpStatus():
            mycansat.stopPump()
    
    
    
    while True:
        
        mycansat.receive()
        
        while mycansat.getCansat():
            
            if mycansat.checkLight():
                checkPump(mycansat)
                mycansat.readTemp()
                mycansat.sendTemp()
                mycansat.receive()
                checkPump(mycansat)
                mycansat.readPressure()
                mycansat.sendPressure()
                mycansat.receive()
                checkPump(mycansat)
                mycansat.readAltitude()
                mycansat.sendAltitude()
                mycansat.receive()
                checkPump(mycansat)
                mycansat.sendPumpStatus()
                mycansat.receive()
                
            

            
