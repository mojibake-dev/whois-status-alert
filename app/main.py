import whois, os, json, boto3, datetime, botocore


################ FUNCTION DEFINITIONS ################

def logging(level, message):
    timeStamp = str(datetime.datetime.now())
    message = f"{timeStamp} - {level} - {message}"
    print(message)


def loadLastStatus(s3, bucketName, key):
    response = s3.get_object(Bucket=bucketName, Key=key)
    content = response['Body'].read().decode('utf-8')
    lastStatus = json.loads(content)
    return lastStatus


def grabStatus(domain):
    status = whois.whois(domain).status
    logging("INFO", f"grabbed status: {status} for domain {domain}")
    return status


def saveStatus(s3, status, bucketName, key="status.json"):
    jsonContent = json.dumps(status)
    s3.put_object(
        Bucket = bucketName,
        Key = key,
        Body = jsonContent.encode('utf-8')
        )
    logging("INFO", f"Logging status {status} to file: {key}")


# TODO: verify arn specificity * 
def emailAlert(client, toAddress, fromAddress, subject, body):

    response = client.send_email(
    Destination={
        'ToAddresses': [toAddress]
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': body,
            }
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': subject,
        },
    },
    Source=fromAddress
    )
    
    print(response)
    
    return {
        'statusCode': 200,
        'body': json.dumps("Email Sent Successfully. MessageId is: " + response['MessageId'])
    }


################ MAIN LOGIC ################
def handler(event, context):

    s3 = boto3.client('s3')
    ses = boto3.client('ses', region_name='us-west-2')

    BUCKET_NAME = os.environ['BUCKET_NAME']
    DOMAIN = os.environ['DOMAIN']
    TO_ADDRESS = os.environ['TO_ADDRESS']
    FROM_ADDRESS = os.environ["FROM_ADDRESS"]
    WHOIS_PAGE = os.environ["WHOIS_PAGE"]
    REQUEST_FORM = os.environ["REQUEST_FORM"]

    status = grabStatus(DOMAIN)

    # check for last status 
    try:
        lastStatus = loadLastStatus(s3, BUCKET_NAME, "status.json")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            logging("WARNING", f"Existing status not found for: {DOMAIN}. Generating first status log.")
            saveStatus(s3, status, BUCKET_NAME, "status.json")
            emailAlert(ses, TO_ADDRESS, FROM_ADDRESS, "WHOIS_ALERT: First Log Taken", f"Existing status not found for: {DOMAIN}. Generating first status log.")
            return
        else:
            raise

    # compare
    if status == lastStatus:
        logging("INFO", f"Recently queried status matches our stored status. Nothing has changed.")
        saveStatus(s3, status, BUCKET_NAME, "status.json")
    else:
        logging("INFO",f"Status for {DOMAIN} has changed!!!")
        saveStatus(s3, status, BUCKET_NAME, "caughtStatus.json")
        emailAlert(ses, TO_ADDRESS, FROM_ADDRESS, "WHOIS_ALERT: DOMAIN STATUS HAS CHANGED!!!!", f"Status for {DOMAIN} has changed!!! \n CHECK WHOIS: {WHOIS_PAGE} \n SUBMIT FORM: {REQUEST_FORM}")

    return {
        'statusCode': 200,
        'body': f"Logged status for {DOMAIN}"
    }
