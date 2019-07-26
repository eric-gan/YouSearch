import boto3
import time

BUCKET = 'yousearchdev'
ACCESS_KEY = 'AKIA4TOXGMUPL2ID4ENZ'
SECRET_ACCESS_KEY = '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'
REGION_NAME = 'us-east-2'
transcribe = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY, 
    aws_secret_access_key=SECRET_ACCESS_KEY, region_name=REGION_NAME)

def transcribe_file(link):
    v_id = link.split('=')[-1]
    job_name = v_id
    job_uri = 'https://' + BUCKET + '.s3.us-east-2.amazonaws.com/' + v_id + '.mp4'
    print(job_uri)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp4',
        LanguageCode='en-US',
        OutputBucketName=BUCKET,
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)

transcribe_file('https://www.youtube.com/watch?v=lzkKzZmRZk8')




