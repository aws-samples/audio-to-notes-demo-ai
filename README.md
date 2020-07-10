# audio-notes-demo

A demonstrantion using Amazon Textextract and Amazon polly to extract text of images and generate audio files for you to hear.

# Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) - Only to run web app locally
- [awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [Pre configured AWS credentials](https://docs.aws.amazon.com/amazonswf/latest/awsrbflowguide/set-up-creds.html)
- [Pre configured VPC with at minimun 2 public subnets]()

# Architecture

<p align="center"> 
<img src="images/ai_diagram_webinar.png">
</p>

# Setup instructions

## Provision the infraestructure

First you need to create a S3 bucket to store our application lambda code. (That will be used in Cloudformation Later)

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

**Now we need to create two stacks using our Cloudformation template available in cloudformation/ folder**

## Lambda Cloudformation Stack

This CF template will provision all the components to extract the text of the image files using Textract and publishes into the s3 bucket to be converted to audio using Polly

```shell
aws cloudformation create-stack --stack-name audio-notes-stack --template-body file://cloudformation/audionotesstack.yaml --parameters ParameterKey=BucketName,ParameterValue=<NEW_BUCKET_NAME> ParameterKey=BucketLambdaCode,ParameterValue=<BUCKET_NAME_THAT_WE_PROVISIONED_BEFORE> --capabilities CAPABILITY_IAM
```

## ECS Cloudformation Stack

This CF template will provision an ECS cluster to host our Web Application that we will use to upload teh images to s3 and download the audio files form S3

```shell
aws cloudformation create-stack --stack-name audio-notes-ecs --template-body file://cloudformation/aecsstack.yaml --parameters ParameterKey=BucketName,ParameterValue=<NEW_BUCKET_NAME> ParameterKey=BucketLambdaCode,ParameterValue=<BUCKET_NAME_THAT_WE_PROVISIONED_BEFORE> --capabilities CAPABILITY_IAM
```


# How our application works

Access the DNS address of the ELB provisioned by our Cloudformation.

# Clean up

# TODO

- Instructions of how to upload Docker image to ECS Registry
- Add VPC with public subnets pre-req and reference to a source repository