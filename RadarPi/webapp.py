from flask import Flask, render_template, request#test git
import datetime
app = Flask(__name__)

@app.route("/")
def home():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'RadarPi | Home',
        'time': timeString,
        'heading':  'Embedded Audio Radar System',
        'body': 'The radar has two options. Continuous Wave and Range-Doppler. \n Select one to continue.'
        }
    return render_template('main.html', **templateData)


@app.route("/cw")
def cw():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'RadarPi | CW',
        'time': timeString,
        'heading':  'Embedded Audio Radar System',
        'subheading': 'Continuous Wave Radar'
        }
    return render_template('main.html', **templateData)



@app.route('/pulsedoppler')
def pulsedoppler():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'RadarPi | PD',
        'time': timeString,
        'heading':  'Embedded Audio Radar System',
        'subheading': 'Pulse-Doppler Wave Radar'
        }
    return render_template('pulsedoppler.html')
    
@app.route('/results',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      results = request.form
      return render_template("results.html",results = results)


if __name__ == "__main__":
    app.run(host='radarpi.local', port=8080, debug=True)