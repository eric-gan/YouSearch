from flask import Flask, request, render_template, redirect, url_for
import os, threading, json

app = Flask(__name__)
@app.route('/', methods=['GET'])
def homepage():
    print('loaded homepage')
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_video():
    print('dklfjal;skdjf')
    video_input = request.form['search']
    print(video_input)
    return results(video=video_input)

@app.route('/results/')
def results(video=None):
    prefix = 'https://www.youtube.com/embed/'
    video_tag = video.split('=')[1]
    video_embed = prefix + video_tag
    return render_template('results.html', video=video_embed)

if __name__ == "__main__":
    app.run(debug=True)