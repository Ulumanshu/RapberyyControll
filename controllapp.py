import RPi.GPIO as GPIO
import os
import flask
from flask import Flask, render_template, url_for, request, flash, redirect,\
    jsonify
from werkzeug.serving import run_simple
import time

app = Flask(__name__)
app.debug = True

GPIO.setmode(GPIO.BOARD)
pin1 = 7
pin2 = 11
GPIO.setup(pin1, GPIO.OUT, initial = 0)
GPIO.setup(pin2, GPIO.OUT, initial = 0)

def read_temp():
    "Read data from Raspberry Pi (specifically read GPU temperature)"
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return "GPU temperature is {}".format(temp[5:])
    
def switch_on(pin):
    GPIO.output(pin, 1)
    
def switch_off(pin):
    GPIO.output(pin, 0)

def check_state(pin):
    if pin:
        state = GPIO.input(pin)
    else:
        state = False
    return state

@app.route("/")
def hello():
    res = 'pins'
    return render_template('home.html', title="Home", temp=read_temp(), value=res)
    
@app.route("/command", methods=["GET", "POST"])
def command():
    res= {"id": False, 'value': False}
    if flask.request.method == "GET":
        response = dict(request.args)
        pin_id = response.get('id') and response.get('id')[0] or False
        if pin_id:
            pin = pin_id[3:].isdigit() and int(pin_id[3:]) or False            
            state = check_state(pin)
            if state:
                switch_off(pin)
                res.update({"id": pin_id, 'value': 'OFF'})
            else:
                switch_on(pin)
                res.update({"id": pin_id, 'value': 'ON'})
    return render_template('home.html', title="Home", temp=read_temp(), value=jsonify(res))
    
if __name__ == "__main__":
    print("Starting!...")
    run_simple("0.0.0.0", 5000, app, use_reloader=True, use_debugger=True, use_evalex=True)

