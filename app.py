import os
from flask import Flask, render_template, request, redirect, send_file
from s3_demo import list_files, download_file, upload_file
from os.path import join, dirname, realpath
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resource={"/*": {"origins": ["*"]}})

UPLOAD_FOLDER = "uploads"
BUCKET = "first-bucket-boto3"


@app.route('/')
def entry_point():
    return 'Welcome to File Management API'


@app.route("/form", methods=['GET'])
def form():
    contents = list_files("first-bucket-boto3")
    return render_template('form.html', contents=contents)


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/form")


@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)


if __name__ == '__main__':
    app.run()
