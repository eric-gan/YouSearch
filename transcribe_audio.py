import time, uuid
import boto3
import utils

transcribe = boto3.client('transcribe', aws_access_key_id=utils.ACCESS_KEY, 
    aws_secret_access_key=utils.SECRET_ACCESS_KEY, region_name=utils.REGION_NAME)

def transcribe_file(video_tag):
    job_uri = 'https://' + utils.BUCKET + '.s3.us-east-2.amazonaws.com/' + video_tag + '.mp4'
    print(job_uri)
    print(video_tag)
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=video_tag,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp4',
            LanguageCode='en-US',
            OutputBucketName=utils.BUCKET,
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=video_tag)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
        print(status)

    except Exception:
        print('Transcription already exists, pulling from S3 bucket')
        return

#transcribe_file('https://www.youtube.com/watch?v=QU3rL5-lj2Y')