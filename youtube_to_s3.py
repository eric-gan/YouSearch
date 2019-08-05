from pytube import YouTube

import boto3
import botocore.vendored.requests.packages.urllib3 as urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import utils

s3 = boto3.client('s3', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)

def fetch_video(link):
    v_id = link.split('=')[-1]
    yt = YouTube(link)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").all()[-1]
    print(stream.url)
    key = v_id + '.mp4'

    http = urllib3.PoolManager()
    s3.upload_fileobj(http.request('GET', stream.url, preload_content=False), utils.BUCKET, key)
    return

#https://www.youtube.com/watch?v=gsC6hB6az10
