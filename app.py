import os
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import list_files, download_file, create_random_id, upload_file_obj
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resource={"/*": {"origins": ["*"]}})
app.config['UPLOAD_EXTENSIONS'] = ['.png', '.jpg', '.jpeg', '.gif']
app.config['MAX_CONTENT_LENGTH'] = 1.4 * 1000 * 1000

UPLOAD_FOLDER = "uploads/"
BUCKET = "first-bucket-boto3"


@app.errorhandler(413)
def too_large(e):
    response = {'ERROR': 'File is too large'}
    return response, 413


@app.route('/')
def entry_point():
    return 'Welcome to File Management API'


@app.route("/form", methods=['GET'])
def form():
    contents = list_files("first-bucket-boto3")
    return render_template('form.html', contents=contents)


@app.route("/upload", methods=['POST'])
def upload():
    response = {}
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename == '':
        response['ERROR'] = "No file name was provided!"
        return response, 400
    else:
        generated_filename = create_random_id(filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext.lower() not in app.config['UPLOAD_EXTENSIONS']:
            response['ERROR'] = f"Accepting file types: {', '.join(app.config['UPLOAD_EXTENSIONS'])}"
            return response, 400
        else:
            try:
                relative_path = UPLOAD_FOLDER + generated_filename
                upload_file_obj(uploaded_file, BUCKET, relative_path)

            except Exception as error:
                response['ERROR'] = str(error)
                status_code = 400
            else:
                response['original_filename'] = uploaded_file.filename
                response['url'] = relative_path
                response['generated_filename'] = generated_filename
                status_code = 200
            # return redirect("/form")
            return response, status_code


@app.route("/downloads/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)


if __name__ == '__main__':
    app.run()
