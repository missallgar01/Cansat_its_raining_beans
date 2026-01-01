from flask import Flask, jsonify, render_template, request, url_for, redirect
from datareader import Datareader
from analysis import Analysis

app = Flask(__name__)

datareader = Datareader()

#Dashboard interface
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/live',methods=('GET', 'POST'))
def live():
    if request.method=="POST":
        if request.form['btn'] == "start":
            print("Read CanSat data")
            sendRequest = 1
            datareader.sendData(sendRequest)

        if request.form['btn'] == "stop":
            print("Stop CanSat data")
            sendRequest = 2
            datareader.sendData(sendRequest)

        elif request.form['btn']=="pumpon":
            print("Light on and turn pump on")
            sendRequest = 3
            datareader.sendData(sendRequest)

        elif request.form['btn'] == "pumpoff":
            print("Light off and turn pump off")
            sendRequest = 4
            datareader.sendData(sendRequest)

        return render_template('live.html')
    
    return render_template('live.html')

@app.get('/update')
def update():

    datareader.readData()
    datareader.processLiveData()
    print("Reading data")
    datareader.saveToFile()
    temp = datareader.getTemp()
    pressure = datareader.getPressure()
    altitude = datareader.getAltitude()
    pumpstatus = datareader.getPumpStatus()
    
    return jsonify(temp=temp,pressure=pressure, altitude=altitude, pumpstatus=pumpstatus)

@app.route('/analysis')
def analysis():

  chart = Analysis()
  df = chart.readCSV()
  chart.chart()
  
  return render_template('analysis.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
