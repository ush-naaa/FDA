# fda_aggregator/config.py
from dotenv import load_dotenv

def load_config():
    """Loads environment variables from the .env file."""
    # load_dotenv() searches the project root for the .env file
    # and makes the variables available via os.environ
    load_dotenv()