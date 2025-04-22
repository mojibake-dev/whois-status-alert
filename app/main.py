import whois, logging, os, json, boto3

################ CONFIG LOGGING ################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
#        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler(),  # Also log to the console 
    ],
)

################ FUNCTION DEFINITIONS ################


def loadLastStatus(s3, bucketName, key):
    response = s3.get_object(Bucket=bucketName, Key=key)
    content = response['Body'].read().decode('utf-8')
    lastStatus = json.loads(content)
    return lastStatus


def grabStatus(domain):
    status = whois.whois(domain).status
    logging.info(f"grabbed status: {status} for domain {domain}")
    return status


def saveStatus(s3, status, bucketName, key="status.json"):
    jsonContent = json.dumps(status)
    s3.put_object(
        Bucket = bucketName,
        Key = key,
        Body = jsonContent.encode('utf-8')
        )
    logging.info(f"Logging status {status} to file: {key}")


def compareStatus(status, lastStatus):
    if status == lastStatus:
        return True
    else:
        return False

def emailAlert():
    print('TEXT ALERT GOES HERE')

################ MAIN LOGIC ################
def main():

    s3 = boto3.client('s3')

    BUCKET_NAME = os.environ['BUCKET_NAME']
    DOMAIN = os.environ['DOMAIN']

    status = grabStatus(DOMAIN)

    # check for last status 
    try:
        lastStatus = loadLastStatus(s3, BUCKET_NAME, "status.json")
    except 'NoSuchKey':
        logging.warning(f"Existing status not found for: {DOMAIN}. Generating first status log.")
        saveStatus(status)
        emailAlert()
        return

    # compare
    if status == lastStatus:
        logging.info(f"Recently queried status matches our stored status. Nothing has changed.")
        saveStatus(status)
    else:
        logging.info(f"Status has changed!!!")
        saveStatus(status, "newStatus.json")
        emailAlert()


################ EXECUTE ################
if __name__ == "__main__":
    main()

