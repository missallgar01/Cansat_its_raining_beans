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
        pass
        self.light = False

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


    def configurePump(self):
        PWM_PIN_A = board.GP19 #AIN2
        PWM_PIN_B = board.GP18 #AIN1
        self.pwm_a = pwmio.PWMOut(PWM_PIN_A,frequency = 50)
        self.pwm_b = pwmio.PWMOut(PWM_PIN_B,frequency = 50)
        self.motor1 = motor.DCMotor(self.pwm_a,self.pwm_b)

    def startPump(self):
        self.motor1.throttle = 1
        print("DC motor test")
        print("\nForwards slow")
        print("throttle:",self.motor1.throttle)


    def stopPump(self):

        self.motor1.throttle = 0
        print("DC motor stop")


if __name__ == '__main__':
    mycansat = Cansat()
    mycansat.configureLight()
    mycansat.configurePump()

    while True:
        if mycansat.checkLight:
            print(mycansat.checkLight())
            print("hellO")
            mycansat.startPump()
            time.sleep(5)
            mycansat.stopPump()
            time.sleep(5)

