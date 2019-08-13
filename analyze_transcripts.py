from botocore.exceptions import ClientError

import json
import boto3
import utils

import youtube_to_s3, transcribe_audio

s3 = boto3.client('s3', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)
comprehend = boto3.client('comprehend', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)


def get_transcripts(video_tag):
    json_filename = video_tag + '.json'
    json_file = s3.get_object(Bucket=utils.BUCKET, Key=json_filename)
    json_content = json_file['Body'].read().decode('utf-8')
    json_data = json.loads(json_content)
    transcript = json_data['results']['transcripts'][0]['transcript']
    word_data = json_data['results']['items']
    return transcript, word_data

def get_times(video_tag, user_word):
    transcript, word_data = get_transcripts(video_tag)
    if user_word not in transcript and user_word.capitalize() not in transcript:
        print('Cannot find word in the video')
        return
    times = []
    for word in word_data:
        if word['type'] != 'pronunciation':
            continue
        if word['alternatives'][0]['content'] == user_word or word['alternatives'][0]['content'] == user_word.capitalize():
            times.append(word['start_time'])
    return times

def get_sentiment(video_tag):
    try:
        s3.head_object(
            Bucket=utils.BUCKET, Key=video_tag+'.mp4')
        print('Found video in S3 bucket, pulling from S3 bucket')
    except ClientError as e:
        print('Video not found in S3 bucket, uploading video from YouTube to S3 bucket')
        download_prefix = 'https://www.youtube.com/watch?v='
        link = download_prefix + video_tag
        youtube_to_s3.fetch_video(link)
        transcribe_audio.transcribe_file(video_tag)

    transcript, _ = get_transcripts(video_tag)
    transcript_length = len(transcript.encode('utf-8'))
    # max length of amazon comprehend request text
    if transcript_length > 5000:
        transcript = str(transcript.encode('utf-8')[:4990])

    sentiment_json = comprehend.detect_sentiment(
        Text=transcript,
        LanguageCode='en')
    sentiment_score, sentiment = sentiment_json['SentimentScore'], sentiment_json['Sentiment']
    return sentiment_score
