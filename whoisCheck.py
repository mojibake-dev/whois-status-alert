import whois, logging, os, pickle
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
    return domain

def loadLastStatus():
    return lastStatus

def grabStatus(domain):
    status = whois.whois(domain).status
    return status

def saveStatus(status):
    return

def compareStatus():
    return check

def main():
    
    domain = loadEnv()

    status = grabStatus(domain)
    #log grabing status 
    
    # check for last status 
    # if no 
        # log 
        # report 
    # if yes 
        # compare
        # if status same
            # log 
            # quit
        # if status different
            # log
            # report
    
    return

if __name__ == "__main__":
    main()