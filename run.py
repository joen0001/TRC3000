# Code to run the local host/server 

from flask import Flask, render_template, request
from main import Initialisation, runall, emergency_stop, power_off

app = Flask(__name__, template_folder=".", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

# Assigning Functions to each button    
@app.route("/forward/", methods=["POST"])
def button_click():
    # Start
    if request.form["button"] == "b1":
        runall()
    # Stop
    if request.form["button"] == "b2":
        emergency_stop(2)
    # Calibration
    if request.form["button"] == "b3":
        Initialisation(3)
    # Power off
    if request.form["button"] == "b4":
        power_off(4)

    return index()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
