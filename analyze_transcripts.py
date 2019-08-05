import json
import boto3
import utils

s3 = boto3.client('s3', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)
comprehend = boto3.client('comprehend', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)


def get_transcripts(link):
    v_id = link.split('=')[-1]
    json_filename = v_id + '.json'
    json_file = s3.get_object(Bucket=utils.BUCKET, Key=json_filename)
    json_content = json_file['Body'].read().decode('utf-8')
    json_data = json.loads(json_content)
    transcript = json_data['results']['transcripts'][0]['transcript']
    word_data = json_data['results']['items']
    return transcript, word_data

def get_times(link, user_word):
    transcript, word_data = get_transcripts(link)
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

def get_sentiment(link):
    transcript, _ = get_transcripts(link)
    sentiment_json = comprehend.detect_sentiment(
        Text=transcript,
        LanguageCode='en')
    sentiment_score, sentiment = sentiment_json['SentimentScore'], sentiment_json['Sentiment']
    print(sentiment_score)
    print(sentiment)


# print(get_sentiment('https://www.youtube.com/watch?v=QU3rL5-lj2Y'))
# print(get_times('https://www.youtube.com/watch?v=QU3rL5-lj2Y', 'just'))