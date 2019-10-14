#!/usr/bin/python3

import waveGenerator
import recordAudio
import cwProcessing
import pdProcessing
from playSound import playSound
from flask import Flask, render_template, request

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

@app.route("/")
@app.route("/radarpi.html")
@app.route("/radarpi")
def home():
    return render_template('radarpi.html')

@app.route("/cwNT.html")
@app.route("/cwNT")
def cwNT():
    return render_template('cwNT.html')

@app.route("/cwT.html")
@app.route("/cwT")
def cwT():
    return render_template('cwT.html')

@app.route("/pulsedopplerNT.html")
@app.route("/pulsedopplerNT")
def pulsedopplerNT():
    return render_template('pulsedopplerNT.html')

@app.route('/pulsedopplerT.html')
@app.route('/pulsedopplerT')
def pulsedopplerT():
    return render_template('pulsedopplerT.html')
    
@app.route('/results.html',methods = ['POST', 'GET'])
def results():
    if request.method == 'POST':
        results = request.form       
        mode = request.form['mode']
      
        try:
            if mode == 'Continuous Non-Technical':
              
                duration = float(request.form["duration"])
                volume = float(request.form["volume"])/100
              
                waveGenerator.waveGenerator(duration)
                name = '8000Hz.wave' 
                playSound(name,volume)
                Rx_Signal = recordAudio.recordAudio(duration*1.1)
                cwProcessing.cwProcessing(Rx_Signal)

                return render_template("results.html",results = results)
          
            elif mode == 'Continuous Technical':
              
                frequency = float(request.form["frequency"])
                duration = float(request.form["duration"])
                volume = float(request.form["volume"])/100

                waveGenerator.waveGenerator(duration, frequency=frequency)
                name = str(int(frequency)) + 'Hz.wave'
                playSound(name,volume)
                Rx_Signal = recordAudio.recordAudio(duration*1.1)
                cwProcessing.cwProcessing(Rx_Signal,frequency=frequency)
              
                return render_template("results.html",results = results)
          
            elif mode == 'Pulse Doppler Non-Technical':
              
                rangeU = float(request.form["rangeU"])
                volume = float(request.form["volume"])/100
                
                Tx_Signal, Tx_p = waveGenerator.pulseTrainGenerator(rangeU)
                name = 'Chirp 8000Hz.wave'
                
                duration = 32 * ((2 * rangeU) / 343) #PRI
    #             print(duration)
                playSound(name,volume)
                Rx_Signal = recordAudio.recordAudio(duration*1.2)
                
                pdProcessing.pdProcessing(Tx_p, Rx_Signal, rangeU)

                return render_template("results.html",results = results)
          
            elif mode == 'Pulse Doppler Technical':
              
                rangeU = float(request.form["rangeU"])
                resolution = float(request.form["resolution"])
                frequency = float(request.form["frequency"])
                bandwidth = float(request.form["bandwidth"])
                pulses = float(request.form["pulses"])
                volume = float(request.form["volume"])/100

                Tx_Signal, Tx_p = waveGenerator.pulseTrainGenerator(rangeU,resolution=resolution,frequency=frequency,bandwidth=bandwidth,numPulses=pulses)

                name = 'Chirp ' + str(int(frequency)) + 'Hz.wave'
                
                duration = pulses * ((2 * rangeU) / 343)

                playSound(name,volume)
                Rx_Signal = recordAudio.recordAudio(duration*1.1)
                
                pdProcessing.pdProcessing(Tx_p, Rx_Signal, rangeU, numPulses=pulses, fc=frequency, bandwidth=bandwidth)

                return render_template("results.html",results = results)
              
            else:
              
                return render_template("none.html")
          
        except:
            return render_template("none.html")
          
      



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
