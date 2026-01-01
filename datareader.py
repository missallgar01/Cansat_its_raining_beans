import serial
import pandas as pd
import csv
from serial.tools import list_ports
class Datareader():

    def __init__(self):
        # Configure the serial connection
        port = list(list_ports.comports())
        for p in port:
            if "usbmodem" in p.device:
                self.port = p.device

        self.ser = serial.Serial(
            port=self.port,  # Change this according to connection methods, e.g. /dev/ttyUSB0
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        self.temp = 0.0
        self.pressure = 0.0
        self.altitude = 0.0
        self.pumpStatus = False

        self.dataList = [self.temp, self.pressure, self.altitude, self.pumpStatus]
        self.datastr = ""
    def sendData(self, data):

        command = str(data) + "\n"
        self.ser.write(bytes(command.encode('ascii')))

    def readData(self):
        self.datastr=""
        if self.ser.in_waiting > 0:
            self.datastr = self.ser.readline()
            self.datastr = self.datastr.decode("utf-8", "ignore").strip()
            print(self.datastr[:-2])

    def processLiveData(self):
            # if first byte in the byte array is temp
        if len(self.datastr) > 0:
            if self.datastr[0] == "1":  # temp
                temp = self.datastr[1:]
                print("temp", temp)
                self.dataList[0] = temp

            elif self.datastr[0] == "2":  # pressure
                pressure = self.datastr[1:]
                print("pressure", pressure)
                self.dataList[1] = pressure

            elif self.datastr[0] == "3":  # altitude
                altitude = self.datastr[1:]
                print("altitude", altitude)
                self.dataList[2] = altitude

            elif self.datastr[0] == "4":  # pumpstatus
                self.pumpStatus = self.datastr[1:]
                print("Pump Status", self.pumpStatus)
                self.dataList[3] = self.pumpStatus

    def saveToFile(self):
        print(self.dataList)
        with open('data/data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            current_time = pd.Timestamp.now()

            writer.writerow([current_time, self.dataList[0], self.dataList[1], self.dataList[2], self.dataList[3]])

    def getTemp(self):
        self.temp = self.dataList[0]
        return self.temp

    def getPressure(self):
        self.pressure = self.dataList[1]
        return self.pressure

    def getAltitude(self):
        self.altitude = self.dataList[2]
        return self.altitude

    def getPumpStatus(self):
        self.pumpStatus = self.dataList[3]
        return self.pumpStatus

    def goodbye(self):
        print("Goodbye!")
        self.ser.close() # Close serial connection

if __name__ == '__main__':

    pass












