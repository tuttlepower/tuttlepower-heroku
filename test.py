from flask import Flask, render_template, session, redirect, url_for, request, jsonify, send_from_directory
import random
import os
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'stuff'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="Post" enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
# @app.route("/", methods=['GET','POST'])
# def home():
#     if request.method =='POST':
#         workout = request.form['workout']
#         reps = request.form['reps']

#         return render_template("workout.html", workouts= workouts.get(workout), max =225)
#     return render_template("index.html")

# @app.route("/<workout>")
# def workout(workout):
#     return render_template("workout.html", workouts=workouts.get(workout))

@app.route("/image", methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        print(request.files['myfile'])
        print('Post happened!')
        return render_template("image.html")

    return render_template("image.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # returns a 200 (not a 404) with the following contents:
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
