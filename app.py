import os
from flask import Flask, render_template, request, redirect, send_file
from s3_demo import list_files, download_file, upload_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resource={"/*": {"origins": ["*"]}})
app.config['UPLOAD_EXTENSIONS'] = ['.png', '.jpg', '.jpeg', '.gif', '.txt']
app.config['MAX_CONTENT_LENGTH'] = 1.4 * 1000 * 1000

UPLOAD_FOLDER = "uploads"
BUCKET = "first-bucket-boto3"


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


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
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext.lower() not in app.config['UPLOAD_EXTENSIONS']:
            response['ERROR'] = f"Accepting file types: {', '.join(app.config['UPLOAD_EXTENSIONS'])}"
            return response
        else:
            uploaded_file = request.files['file']
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, uploaded_file.filename))
            upload_file(f"uploads/{uploaded_file.filename}", BUCKET)
            data = {'file_name': uploaded_file.filename, 'url': f'uploads/{uploaded_file.filename}'}
            # return redirect("/form")
            return data


@app.route("/downloads/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)


if __name__ == '__main__':
    app.run()
