import pandas as pd
import matplotlib.pyplot as plt
import math

class Analysis():
    
    def __init__(self):

        pass

    def readCSV(self):
    
        self.df = pd.read_csv('data/data.csv')


    def chart(self):

        self.df.plot(kind='line', x='temp', y='altitude')
        plt.xlabel("Temp")
        plt.ylabel("Altitude")
        plt.savefig('static/images/tempchart.png')

    def calculateImpact(self):
        
        maxAlt = self.df.loc[self.df['altitude'].idxmax()]
        #print(maxAlt)
        s=maxAlt
        u=0
        a=9.81
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['time_diff'] = self.df['timestamp'].diff()
        vSquared=u**2+2*a*s
        v = math.sqrt(vSquared)
        return v

if __name__ == '__main__':
    pass
