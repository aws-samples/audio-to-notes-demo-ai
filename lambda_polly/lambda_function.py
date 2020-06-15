import boto3
import os
from datetime import datetime
import json

def change_text_to_audio(client, text):

    response = client.synthesize_speech(
        LanguageCode='pt-BR',
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId='Ricardo'
    )
    return response


def change_audio_stream(response, audio_id):
    file = open(f"/tmp/{audio_id}.mp3", 'wb')
    file.write(response['AudioStream'].read())
    file.close()


def aws_connection(service="polly", region_name="us-east-1"):
    client = boto3.client(service, region_name=region_name)
    return client


def send_audio_to_s3(audio_file, description, file_name, bucket_name):
    try:
        s3 = boto3.resource('s3')
        response = s3.meta.client.upload_file(audio_file, bucket_name, f"polly_output/{file_name}.mp3")
    except Exception as e:
        raise e


def lambda_handler(event, context):
    print(event)
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y")
    # TODO get this variables from event source
    text_to_audio = event["responsePayload"]["message"]
    
    audio_id = f"{text_to_audio[:20].replace(' ', '')}{date_time}"
    bucket_name = os.getenv("BUCKET_NAME", "ai-services-for-demo")

    polly_client = aws_connection()
    audio_response = change_text_to_audio(polly_client, text_to_audio)
    change_audio_stream(audio_response, audio_id)

    send_audio_to_s3(f"/tmp/{audio_id}.mp3", 
        text_to_audio[:100], audio_id, bucket_name)