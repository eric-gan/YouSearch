from flask import Flask, request, render_template, redirect, url_for
import os, threading, json

app = Flask(__name__)
@app.route('/', methods=['GET'])
def homepage():
    print('loaded homepage')
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_video():
    video_input = request.form['search']
    print(video_input)
    return render_video(video=video_input)

@app.route('/results/')
def render_video(video=None):
    prefix = 'https://www.youtube.com/embed/'
    try:
        video_tag = video.split('=')[1]
    except:
        print('Please enter a valid YouTube link')
        return render_template('index.html')
    video_embed = prefix + video_tag
    return render_template('results.html', video=video_embed)

if __name__ == "__main__":
    app.run(debug=True)