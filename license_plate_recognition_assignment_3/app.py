import os
from flask import Flask, flash, render_template, request, redirect
from werkzeug.utils import secure_filename
from s3Uploader import upload_file_tos3, list_files, grant_public_access
import mturk_client
import boto3

UPLOAD_FOLDER1 = 'C:/Users/Ashmita/Desktop/Data pipeline/Assignment3'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
BUCKET = 'info7374-image-detection'
ACCESS_SECRET_KEY = 'asdasdasdas'
rek = boto3.client('rekognition', region_name="us-east-1")

app = Flask(__name__)
app.secret_key = "secret key"


@app.route("/")
def home():
    return render_template("UploadImage.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            upload_file_tos3(f"{file.filename}", BUCKET, file)
            grant_public_access(BUCKET, file.filename)
            mturk_client.create_hit(BUCKET, file.filename, False)
            flash('File successfully uploaded.')
            return redirect('/storage')
        else:
            flash('Allowed file types are png, jpg, jpeg')
            return redirect(request.url)


@app.route('/infer<filename>', methods=['GET'])
def showInference():
    # detectTextfromImage()
    return render_template("Inference.html")


@app.route("/storage")
def storage():
    contents = list_files("info7374-image-detection")
    return render_template('UploadImage.html', contents=contents)


if __name__ == "__main__":
    app.run(debug=True)
