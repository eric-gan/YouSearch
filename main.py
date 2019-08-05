from flask import Flask, request, render_template, redirect, url_for
from botocore.exceptions import ClientError

import os, threading, json
import boto3

import youtube_to_s3, analyze_transcripts, utils

s3 = boto3.client('s3', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)

app = Flask(__name__)
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_video():
    video_input = request.form['search']
    try:
        video_tag = video_input.split('=')[1]
    except:
        print('Please enter a valid YouTube link')
        return redirect('/')
    return redirect(url_for('results', video_tag=video_tag))

@app.route('/results/<video_tag>', methods=['GET', 'POST'])
def results(video_tag):
    # to utilize within HTML need to change from "watch" tag to "embed"  
    prefix = 'https://www.youtube.com/embed/'
    video = prefix + video_tag
    if request.method == 'GET':
        return render_template('results.html', video=video)
    elif request.method == 'POST':
        try:
            s3.head_object(
                Bucket=utils.BUCKET, Key=video_tag+'.mp4')
            print('found')
        except ClientError as e:
            youtube_to_s3.fetch_video(video)
            print('not found')
        print(request.form['word_search'])
    return render_template('results.html', video=video)

if __name__ == "__main__":
    app.run(debug=True)