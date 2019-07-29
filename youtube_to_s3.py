from pytube import YouTube

import boto3
import botocore.vendored.requests.packages.urllib3 as urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ACCESS_KEY = 'AKIA4TOXGMUPL2ID4ENZ'
SECRET_ACCESS_KEY = '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'
BUCKET = 'yousearchdev'
REGION_NAME = 'us-east-2'
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, 
    aws_secret_access_key=SECRET_ACCESS_KEY, region_name=REGION_NAME)

def download_video(link):
    v_id = link.split('=')[-1]
    yt = YouTube(link)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").all()[-1]
    print(stream.url)
    key = v_id + '.mp4'

    http = urllib3.PoolManager()
    s3.upload_fileobj(http.request('GET', stream.url, preload_content=False), BUCKET, key)
    return

print(download_video('https://www.youtube.com/watch?v=QU3rL5-lj2Y'))
