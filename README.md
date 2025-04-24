# whois-status-alert

## The Problem

This project is a script to periodically check a domain's status. 

There is a domain I would like, however it currently has the following bizarre statuses. 

'''
  Domain Status: DeleteProhibited
  Domain Status: Hold
  Domain Status: Locked
  Domain Status: RegistrantTransferProhibited
'''

this is because it is locked due to its involvement in multiple romanian court cases. 
I would like to know when it frees up, but a lot of domain brokers do not truck in .ro domains.

So I have built this myself.

## The Solution

TODO: detail. 

TODO: This code will evolve over time to be hosted on AWS and ultimately alert via text

## security concerns

#### Deserialization Attack
Even though the log of the last time the whois was queried is not public facing and it's highly unlikely to be tampered with, we've opted not to use pickle as quoting from python's docs here: https://docs.python.org/3/library/pickle.html

> Warning
> The pickle module is not secure. Only unpickle data you trust.
> It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never unpickle data that could have come from an untrusted  source, or that could have been tampered with.
> Consider signing data with hmac if you need to ensure that it has not been tampered with.
> Safer serialization formats such as json may be more appropriate if you are processing untrusted data. See Comparison with json.

as we only need to store a simple list, json will suffice. 

#### Chat GPT recommends vulnerable python docker image 

when consulting openAI (yes I know, but sometimes its useful for synthesizing examples of multiple interoperable parts in ways that documentation or forum posts fall short.) The generated code suggested this code block. 

however python 3.11-slim suffers from a critical vulnerability listed here [https://hub.docker.com/layers/library/python/3.11-slim/images/sha256-974cb5b34070dd2f5358ca1de1257887bec76ba87f6e727091669035e5f3484d]

'''
FROM public.ecr.aws/lambda/python:3.11
'''

#### Environment Variables
Any variables for URL's , the domain queried, or AWS resource names are obfuscated as environment variables and are not represented in source code. 

## High Level Overview of Steps

DEV
- work out script logic on local machine

DEVOPS
- configure as docker image
- create repository in AWS 
- set up pipeline to compile image and push to repository
  - create user 
  - create policy with permissions needed for pipeline
  - create pipeline group and apply policy
  - create add user to group
  - create access keys and configure as secrets in github pipeline 
  - use template in for github workflow to build docker image and push to repository 
  - test and troubleshoot
- create s3 bucket
- create lamda 
  - use docker image
  - add repository access to lambda permissions
  - add s3 bucket access to lambda permissions
- create logging and add access to lambda permissions
- create SES instance 
  - add custom domain name 
  - perform DKIM authentication to validate domain
  - send test email

DEV
- replace code in local version that grabs json files from local file system to use `boto3` library instead 
- modify logging to print to console
- replace dummy alert messages

TODO: finish documentation of steps

## Helpful Documentation 

- AWS
  - https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#configuration-images-permissions
  - https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-push-iam.html
  - dhttps://repost.aws/knowledge-center/lambda-send-email-ses
  - https://repost.aws/knowledge-center/lambda-ecr-image
  - https://docs.aws.amazon.com/lambda/latest/dg/with-eventbridge-scheduler.html 

- External
  - https://medium.com/@denissedamian/step-by-step-guide-to-ci-cd-for-aws-lambda-with-docker-and-github-actions-c02a9726fd44