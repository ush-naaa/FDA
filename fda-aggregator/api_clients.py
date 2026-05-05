import os
import requests
import logging
from abc import ABC, abstractmethod
from requests.exceptions import RequestException

# Setup logger for this module
# Note: Basic config is usually done once in main, but defined here for robust logging in this file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AbstractDataClient(ABC):
    """
    Abstract Base Class for all external API clients. 
    Defines the contract for fetching data and handles common errors.
    (Requirement 3.1.1: Abstraction/Modularity)
    """
    
    def __init__(self, base_url: str):
        # Base URL is protected (Requirement 3.1.2: Encapsulation)
        self._base_url = base_url

    @abstractmethod
    def fetch_data(self, **kwargs) -> dict:
        """
        Abstract method to be implemented by concrete clients.
        Must fetch raw data from the external API and return a dictionary.
        """
        pass
    
    def _handle_request_error(self, response: requests.Response, api_name: str):
        """
        Handles common HTTP errors (4xx, 5xx) for all clients.
        (Requirement 3.3.1: API Failure)
        """
        if response.status_code != 200:
            error_message = (f"{api_name} API Error. Status: {response.status_code}, "
                             f"Detail: {response.text[:100]}...")
            logger.error(error_message) 
            
            # This automatically raises the correct HTTPError (e.g., 404, 401)
            response.raise_for_status()

class WeatherClient(AbstractDataClient):
    """
    Concrete client for OpenWeatherMap API. 
    Fetches current weather data for a specified city.
    """
    
    def __init__(self):
        # 3.1.2: Encapsulation - Load URL/Key from environment variables
        base_url = os.getenv("OPENWEATHERMAP_URL", "https://api.openweathermap.org/data/2.5/weather")
        self._api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        super().__init__(base_url)
        
        # Check for missing API key (pre-flight check)
        if not self._api_key:
            # Raise a specific error if the configuration is incomplete
            raise ValueError("FATAL: OPENWEATHERMAP_API_KEY is not set. Check your .env file.")

    def fetch_data(self, city_name: str) -> dict:
        """
        Fetches current weather data for a given city.
        """
        logger.info(f"Fetching weather for: {city_name}")
        params = {
            'q': city_name,
            'appid': self._api_key,
            'units': 'metric' 
        }
        
        try:
            # 3.3.2: Network Failure - Catch connection issues and timeout
            response = requests.get(self._base_url, params=params, timeout=10)
            
            # Check for 4xx/5xx errors using the base class method
            self._handle_request_error(response, "OpenWeatherMap")
            
            return response.json()
            
        except RequestException as e:
            # Catch all network-related errors (Connection, Timeout, DNS, etc.)
            logger.error(f"Network or request error for OpenWeatherMap: {e}")
            raise

class MusicClient(AbstractDataClient):
    """
    Concrete client for iTunes Search API. 
    Searches for music albums based on a keyword. (No API key required).
    """
    
    def __init__(self):
        base_url = os.getenv("ITUNES_URL", "https://itunes.apple.com/search")
        super().__init__(base_url)

    def fetch_data(self, search_term: str) -> dict:
        """
        Searches iTunes for music/albums based on a search term.
        """
        logger.info(f"Fetching music for keyword: {search_term}")
        params = {
            'term': search_term,
            'entity': 'album',
            'limit': 3 
        }
        
        try:
            response = requests.get(self._base_url, params=params, timeout=10)
            
            # Check for 4xx/5xx errors
            self._handle_request_error(response, "iTunes Search")
            return response.json()
            
        except RequestException as e:
            logger.error(f"Network or request error for iTunes Search: {e}")
            raise