from flask import Flask, request, render_template, redirect, url_for
from botocore.exceptions import ClientError

import os, threading, json
import datetime

import boto3
import youtube_to_s3, transcribe_audio, analyze_transcripts, utils

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
    # if the post request comes from the sentiment analysis button
    if 'sentiment_button' in request.form:
        sentiment = analyze_transcripts.get_sentiment(video_tag)
        values = list(sentiment.values())
        labels = ['Mixed', 'Positive', 'Neutral', 'Negative']
        colors = ["#EAB126", "#1B7B34", "#1FB58F", "#F24C4E",]
        return render_template('results.html', video=video_tag, values=values, labels=labels, colors=colors)

    if request.method == 'GET':
        return render_template('results.html', video=video_tag, values=[], labels=[], colors=[])

    elif request.method == 'POST':
        try:
            s3.head_object(
                Bucket=utils.BUCKET, Key=video_tag+'.mp4')
            print('Found video in S3 bucket, pulling from S3 bucket')
        except ClientError as e:
            print('Video not found in S3 bucket, uploading video from YouTube to S3 bucket')
            download_prefix = 'https://www.youtube.com/watch?v='
            link = download_prefix + video_tag
            youtube_to_s3.fetch_video(link)
        
        # start transcription of video
        transcribe_audio.transcribe_file(video_tag)
        user_word = request.form['word_search']
        times = analyze_transcripts.get_times(video_tag, user_word)
        if times is None:
            print('No instances of the word found. Try searching again')
            return render_template('results.html', video=video_tag, zipped_times=[], values=[], labels=[], colors=[])

        display_times = [str(datetime.timedelta(seconds=round(float(time)))) for time in times]
        zipped_times = zip(times, display_times)
        return render_template('results.html', video=video_tag, zipped_times=zipped_times, values=[], labels=[], colors=[])

    return render_template('results.html', video=video_tag, values=[], labels=[], colors=[])

if __name__ == "__main__":
    app.run(debug=True)
