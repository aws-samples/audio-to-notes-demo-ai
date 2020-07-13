# audio-notes-demo

A demonstrantion using Amazon Textextract and Amazon polly to extract text of images and generate audio files for you to hear.

# Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) - Only to run web app locally
- [awscli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [Pre configured AWS credentials](https://docs.aws.amazon.com/amazonswf/latest/awsrbflowguide/set-up-creds.html)
- [Pre configured VPC with minimun of 2 public subnets]()

# Architecture

<p align="center"> 
<img src="images/ai_diagram_webinar.png">
</p>

# Provision the infrastructure

First you need to create a S3 bucket to store our application lambda code. (That will be used in CloudFormation Later)

**Note:** Replace <MY_BUCKET_NAME> to a bucket name that you want. (It will be used later)

```shell
aws s3 mb s3://<MY_BUCKET_NAME>
```

ZIP lambda code.

```shell
cd lambda_textract/ && zip ../lambda_textract.zip lambda_function.py
```

```shell
cd ../lambda_polly && zip ../lambda_polly.zip lambda_function.py
```

```shell
cd ../
```
Upload the lambda packages to the S3 bucket that we created before.

```shell
aws s3 cp lambda_textract.zip s3://<MY_BUCKET_NAME>/lambda/
```

```shell
aws s3 cp lambda_polly.zip s3://<MY_BUCKET_NAME>/lambda/
```

**Now we need to create two stacks using our CloudFormation template available in cloudFormation/ folder**

# Lambda Stack

This CloudFormation template will provision all the components to extract the text of the image files using Textract and publishes into the s3 bucket to be converted to audio using Polly

- Run the follow command to provision the first structure to our demo, replace all values inside **<>**

```shell
aws cloudformation create-stack --stack-name audio-notes-stack --template-body file://cloudformation/audionotesstack.yaml --parameters ParameterKey=BucketName,ParameterValue=<NEW_BUCKET_NAME> ParameterKey=BucketLambdaCode,ParameterValue=<BUCKET_NAME_THAT_WE_PROVISIONED_BEFORE> --capabilities CAPABILITY_IAM
```

- After the provisioning log into the AWS console and in **Services** go to CloudFormation

- Search for **audio-notes-stack** and click on it, go to the **Outputs** tab and get the **BucketName** and the **ECRRepositoryArn** they will be useful in the next steps

<p align="center"> 
<img src="images/audio_notes_cf_stack.png">
</p>

# ECS Stack

Before we create our ECS cluster stack we need to create and push the Docker image of our web application to ECR Repository that we created before

- In the AWS console search for ECR in services tab.

- Look for the ECR repository that we created with the stack before the name will be **python-polly-textract** click on it

- Click on **View push commands**

<p align="center"> 
<img src="images/ecr_repository_image.png">
</p>

- Go to **web_app/** and follow the instructions above, that will push to ECR a Docker image with a tag latest

- The result should be this

<p align="center"> 
<img src="images/ecr_with_image.png">
</p>

- Copy the Image URI we will use it later on in the demo

## Provision the ECS Cluster

This CloudFormation template will provision an ECS cluster to host our Web Application that we will use to upload teh images to s3 and download the audio files from S3

```shell
aws cloudformation create-stack --stack-name audio-notes-ecs --template-body file://cloudformation/ecsstack.yaml --parameters ParameterKey=ServiceName,ParameterValue=<SERVICE_NAME> ParameterKey=ImageUrl,ParameterValue=<ECR_IMAGE_URL> ParameterKey=BucketName,ParameterValue=<BUCKET_CREATED_ABOVE_BY_CF> ParameterKey=VpcId,ParameterValue=<ID_OF_VPC_TO_PROVISION_OUR_CLUSTER> ParameterKey=VpcCidr,ParameterValue=<CIDR_OF_THE_VPC> ParameterKey=PubSubnet1Id,ParameterValue=<ID_OF_THE_FIRST_PUB_SUB> ParameterKey=PubSubnet2Id,ParameterValue=<ID_OF_THE_SECOND_PUB_SUB> --capabilities CAPABILITY_IAM
```

- The command above will look like this

```shell
aws cloudformation create-stack --stack-name audio-notes-ecs --template-body file://cloudformation/ecsstack.yaml --parameters ParameterKey=ServiceName,ParameterValue=python-service ParameterKey=ImageUrl,ParameterValue=xxxxxxx.dkr.ecr.XXXX.amazonaws.com/python-polly-textract:latest ParameterKey=BucketName,ParameterValue=textract-polly-demo-aapds ParameterKey=VpcId,ParameterValue=vpc-xxxxxxxxxx ParameterKey=VpcCidr,ParameterValue=X.X.X.X/X ParameterKey=PubSubnet1Id,ParameterValue=subnet-xxxxxxxx ParameterKey=PubSubnet2Id,ParameterValue=subnet-xxxxxxxx --capabilities CAPABILITY_IAM
```

- Access the AWS console and go to **Services>CloudFormation>audio-notes-ecs>Outputs** get the Load Balancer DNS to access out application in browser

<p align="center"> 
<img src="images/alb_dns_name.png">
</p>


# How our application works

Access the DNS address of the ELB provisioned by our CloudFormation.

- Go to Upload Image in the App menu

<p align="center"> 
<img src="images/app_upload_image.png">
</p>

- Select an Image to Upload, that will trigger the process of the Architecture Diagram above and convert the image text to audio.

- You will see the audio file and you will be able to Download it and listen

<p align="center"> 
<img src="images/app_audio.png">
</p>

# Clean up

- Delete all files inside of our provisioned bucket.

```shell
aws s3 rm s3://<BUCKET_NAME_THAT_WAS_PROVISIONED_BY_CF> --recursive
```

- Delete the image inside our ECR Repository

- Delete the CloudFormation stacks

```shell
aws cloudformation delete-stack --stack-name audio-notes-stack
```

```shell
aws cloudformation delete-stack --stack-name audio-notes-ecs
```

- Delete bucket that we used to store our lambda code.

```shell
aws s3 rb s3://<MY_BUCKET_NAME> --force
```