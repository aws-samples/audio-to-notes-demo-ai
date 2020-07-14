from flask import Flask, render_template, jsonify, \
    request, Response, redirect, url_for, session
import random
import boto3
import os

# Flask configurations
app = Flask(__name__)

# Constants
BUCKET_NAME = os.getenv("BUCKET_NAME","ai-services-for-demo")
S3_CLIENT = boto3.client('s3')
OUTPUT_PREFIX = "polly_output/"
INPUT_PREFIX = "textract_input/"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/show_audio_files/', methods=['GET'])
def show_audio_files():
    response = S3_CLIENT.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=OUTPUT_PREFIX,
    )

    list_bucket_objects = []
    print(f"[INFO] Get audio files from S3 Bucket {BUCKET_NAME}")

    for objects in response['Contents']:
        object_name = objects["Key"]
        if object_name != OUTPUT_PREFIX:
            object_name = object_name.split("/")[1]
            list_bucket_objects.append(object_name)
    
    audios_dict_url = {}

    for audios in list_bucket_objects:
        response = S3_CLIENT.generate_presigned_url('get_object',
                    Params={'Bucket': BUCKET_NAME,
                    'Key': f"{OUTPUT_PREFIX}{audios}"},
                    ExpiresIn=3600)
        audios_dict_url[audios] = response
    
    return render_template("audio_files.html", audios_dict_url=audios_dict_url)

@app.route('/upload_s3_image/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # TODO Generate random name for the file
        my_file = request.files['file']
        my_file_name = my_file.filename
        file_name = f"/tmp/{my_file.filename}"
        my_file.save(file_name)

        response = S3_CLIENT.upload_file(file_name, BUCKET_NAME, f"{INPUT_PREFIX}{my_file_name}")
        print(response)

    return render_template("upload_file.html")


app.run(debug=True, host='0.0.0.0')