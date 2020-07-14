import boto3
import os

def aws_connection(service="textract", region_name="us-east-1"):
    client = boto3.client(service, region_name=region_name)
    return client


def extract_information(response):
    words = []
    for block in response["Blocks"]:
        if block['BlockType'] == 'WORD':
            words.append(block['Text'])

    setence = " ".join(words)
    return setence
    

def extract_text(client, bucket_name, object_key):
    response = client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key,
            }
        },
        FeatureTypes=['TABLES','FORMS']
    )
    return response


def lambda_handler(event, context):
    
    # TODO get this variables from event source
    bucket_name = os.getenv("BUCKET_NAME", "ai-services-for-demo")
    lambda_name = os.getenv("LAMBDA_NAME", "lamda_polly")

    object_key = event['Records'][0]['s3']['object']['key']

    print(f"[INFO] Object key {object_key}")
    
    textract_client = aws_connection()
    textract_json = extract_text(textract_client, bucket_name, object_key)
    setence_extracted = extract_information(textract_json)

    lambda_client = aws_connection(service="lambda")
    lambda_input = {"message" : setence_extracted}
    
    return lambda_input