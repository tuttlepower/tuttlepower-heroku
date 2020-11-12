from flask import Flask, render_template,session, redirect, url_for, request,jsonify
import random



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

def dice_roll():
    random_number = random.randint(1, 6)
    if(random_number==1):
        random_number='one'
    if(random_number==2):
        random_number='two'
    if(random_number==3):
        random_number='three'
    if(random_number==4):
        random_number='four'
    if(random_number==5):
        random_number='five'
    if(random_number==6):
        random_number='six'

    return random_number

@app.route('/roll')
def roll():
    return render_template('roll.html', die1 = dice_roll(), die2 =dice_roll())

@app.route('/maps/election/<year>')
def map(year):
    # 
    #need to add upper fence logic
    return render_template('map.html', year = year)
 
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # returns a 200 (not a 404) with the following contents:
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)