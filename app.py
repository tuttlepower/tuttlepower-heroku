from flask import Flask, render_template,session, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/graphs")
def graphs():
    return render_template("graphs.html")

@app.route("/maps")
def maps():
    return render_template("maps.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # returns a 200 (not a 404) with the following contents:
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)