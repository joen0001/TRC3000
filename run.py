from flask import Flask, render_template, request
#from mainNew import runall

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=".", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/forward/", methods=["POST"])
def button_click():
    if request.form["button"] == "b1":
        print(1)
    if request.form["button"] == "b2":
        print(2)
    if request.form["button"] == "b3":
        print(3)
    if request.form["button"] == "b4":
        print(4)
    if request.form["button"] == "b5":
        print(5)
    if request.form["button"] == "b6":
        print(6)

    return index()

if __name__ == "__main__":
    app.run(debug=True)