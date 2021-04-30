from flask import Flask, render_template,session, redirect, url_for, request,jsonify,send_from_directory
import flask_login
from flask_login import LoginManager
import random
import os
from datetime import datetime
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!


login_manager = LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'admin': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("upload.html")

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
@flask_login.login_required
def roll():
    return render_template('roll.html', die1 = dice_roll(), die2 =dice_roll())

@app.route('/maps/election/<year>')
def map(year):
    # 
    #need to add upper fence logic
    return render_template('map.html', year = year)

@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template("protected.html", name = flask_login.current_user.id)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

if __name__ == "__main__":
    app.run(debug=True)

