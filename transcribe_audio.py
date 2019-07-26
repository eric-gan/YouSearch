import boto3

ACCESS_KEY = 'AKIA4TOXGMUPL2ID4ENZ'
SECRET_ACCESS_KEY = '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'
s3 = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)

def transcribe(link):
    v_id = link.split('=')[-1]




