from flask import Flask, render_template, request
app = Flask(__name__)
app._static_folder = "Users/dewanpieterse/Documents/MATLAB/EEE4022S/Audio\ Radar/AudioRadar/RadarPi/templates"

@app.route("/radarpi.html")
def home():
    return render_template('radarpi.html')


@app.route("/cwNT.html")
def cwNT():
    return render_template('cwNT.html')


@app.route("/cwT.html")
def cwT():
    return render_template('cwT.html')


@app.route("/pulsedopplerNT.html")
def pulsedopplerNT():
    return render_template('pulsedopplerNT.html')



@app.route('/pulsedopplerT.html')
def pulsedopplerT():
    return render_template('pulsedopplerT.html')





    
@app.route('/results.html',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      results = request.form
      return render_template("results.html",results = results)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)#host='radarpi.local'