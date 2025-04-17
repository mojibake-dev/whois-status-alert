import whois, logging, os, json
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler(),  # Also log to the console 
    ],
)


def loadEnv():
    load_dotenv()
    domain = os.getenv("DOMAIN")
    logging.info(f"Loading domain {domain} from .env")
    return domain


def loadLastStatus():
    with open('status.json') as file:
        lastStatus = json.load(file)
    return lastStatus


def grabStatus(domain):
    status = whois.whois(domain).status
    logging.info(f"grabbed status: {status} for domain {domain}")
    return status


def saveStatus(status, fileName="status.json"):
    with open(fileName, 'w') as file:
        json.dump(status, file)
    logging.info(f"Logging status {status} to file: {fileName}")


def compareStatus(status, lastStatus):
    if status == lastStatus:
        return True
    else:
        return False


def main():
    
    domain = loadEnv()

    status = grabStatus(domain)
    logging

    # check for last status 
    try:
        lastStatus = loadLastStatus()
    except FileNotFoundError:
        logging.warning(f"Existing status not found for: {domain}. Generating first status log.")
        saveStatus(status)
        # TODO: send text alert
        return

    # compare
    if status == lastStatus:
        logging.info(f"Recently queried status matches our stored status. Nothing has changed.")
        saveStatus(status)
    else:
        logging.info(f"Status has changed!!!")
        saveStatus(status, "newStatus.json")
        # TODO: send text alert.


if __name__ == "__main__":
    main()