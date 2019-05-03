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
pins = [7, 11]
GPIO.setup(pin1, GPIO.OUT, initial = 0)
GPIO.setup(pin2, GPIO.OUT, initial = 0)

def read_temp():
    "Read data from Raspberry Pi (specifically read GPU temperature)"
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return "GPU temperature is {}".format(temp[5:])
    
def switch_on(pin, pin_id):
    res= {"id": False, 'value': False}
    GPIO.output(pin, 1)
    res.update({"id": pin_id, 'value': 'ON'})
    return jsonify(
        success=True,
        data=res
    )
    
def switch_off(pin, pin_id):
    res= {"id": False, 'value': False}
    GPIO.output(pin, 0)
    res.update({"id": pin_id, 'value': 'OFF'})
    return jsonify(
        success=True,
        data=res
    )    

def check_state(pin):    
    state = GPIO.input(pin)    
    return state

@app.route("/")
def hello():
    res7 = check_state(pin1) and "ON" or "OFF"
    res11 = check_state(pin2) and "ON" or "OFF"
    return render_template(
        'home.html', title="Home",
        temp=read_temp(),
        pin7s=res7,
        pin11s=res11
    )
    
@app.route("/command/<string:pin_id>", methods=["GET"])
def command(pin_id):    
    pin = pin_id[3:].isdigit() and int(pin_id[3:]) or False
    if pin in pins:            
        state = check_state(pin)
        if state:
            return switch_off(pin, pin_id)                
        else:
            return switch_on(pin, pin_id)
    else:
        return jsonify(success=False)    
    
if __name__ == "__main__":
    print("Starting!...")
    run_simple("0.0.0.0", 5000, app, use_reloader=True, use_debugger=True, use_evalex=True)

