# audio-notes-demo

A demonstrantion using Amazon Textextract and Amazon polly to extract text of images and generate audio files for you to hear.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [Pre configured AWS credentials](https://docs.aws.amazon.com/amazonswf/latest/awsrbflowguide/set-up-creds.html)

## Architecture

<p align="center"> 
<img src="images/ai_diagram_webinar.png">
</p>

## Setup instructions

### Provision the infraestructure

You just need to run the cloudformation template to provision the infraestructure and all components

First you need to create a S3 bucket to store our application lambda code.

**Note:** Replace <MY_BUCKET_NAME> to a bucket name that you want. (It will be used later)

```shell
aws s3 mb s3://<MY_BUCKET_NAME>
```

ZIP lambda code.

```shell
zip ./lambda_textract.zip lambda_textract/lambda_function.py
```

```shell
zip ./lambda_polly.zip lambda_polly/lambda_function.py
```

Upload the lambda packages to the S3 bucket that we created before.

```shell
aws s3 cp lambda_textract.zip s3://<MY_BUCKET_NAME>/lambda/
```

```shell
aws s3 cp ./lambda_polly.zip s3://<MY_BUCKET_NAME>/lambda/
```

Now we need to create the stack using our Cloudformation template available in **cloudformation/** folder

```shell
aws cloudformation create-stack --stack-name sattelite-rekognition-stack --template-body file://cloudformation/audionotesstack.yaml --parameters ParameterKey=BucketName,ParameterValue=<NEW_BUCKET_NAME> ParameterKey=BucketLambdaCode,ParameterValue=<BUCKET_NAME_THAT_WE_PROVISIONED_BEFORE> --capabilities CAPABILITY_IAM
```

## How our application works

Access the DNS address of the ELB provisioned by our Cloudformation.

## TODO

- Create ECS structure in Cloudformation and Output ELB.