import logging
import os 
from .api_clients import WeatherClient, MusicClient 
from requests.exceptions import RequestException, HTTPError

# Setup basic logging 
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataAggregator:
    """
    The central class responsible for orchestrating API calls, 
    performing data transformation, and unifying the final result.
    (Requirement 3.1.3: Aggregation Class)
    """
    def __init__(self):
        # Instantiate the clients (this calls the __init__ in api_clients.py)
        try:
            self.weather_client = WeatherClient()
            self.music_client = MusicClient()
            logger.info("API Clients initialized successfully.")
        except ValueError as e:
            # Catch error if the API key was missing during client creation
            logger.error(f"Initialization Error: {e}")
            raise # Re-raise to stop execution if configuration is bad

    def _get_music_keyword(self, weather_data: dict) -> str:
        """
        Transforms raw weather data into a music search keyword (Core Transformation).
        (Requirement 2: Transformation/Analysis)
        """
        # 3.3.3: Data Structure Validation: Safely extract the main weather condition
        try:
            # Safely access nested keys using .get() with defaults
            main_condition = weather_data.get('weather', [{}])[0].get('main', 'Unknown').lower()
            temp = weather_data.get('main', {}).get('temp', 20)
        except Exception as e:
            logger.error(f"Error validating weather data structure: {e}")
            return "Ambient Focus Music" # Fallback keyword

        # Rule-based mapping to a music genre/mood
        if 'rain' in main_condition or 'drizzle' in main_condition:
            keyword = "Rainy Day Jazz"
        elif 'clear' in main_condition and temp >= 25:
            keyword = "Upbeat Summer Pop"
        elif 'clear' in main_condition or 'sun' in main_condition:
            keyword = "Road Trip Music"
        elif 'cloud' in main_condition:
            keyword = "Chillhop Playlist"
        else:
            keyword = "Ambient Focus Music"

        logger.info(f"Weather '{main_condition}' mapped to music keyword: '{keyword}'")
        return keyword
    
    def get_recommendation(self, city_name: str) -> dict:
        """
        Orchestrates the data flow: Weather -> Keyword -> Music.
        Calls methods from different clients and performs unification.
        """
        unified_data = {}
        
        # 1. Fetch Weather Data
        try:
            weather_raw = self.weather_client.fetch_data(city_name)
            
            # Summarize weather data for clean output
            weather_summary = {
                'city': weather_raw.get('name', city_name),
                'temperature_c': weather_raw.get('main', {}).get('temp'),
                'condition': weather_raw.get('weather', [{}])[0].get('description', 'Unknown'),
            }
            unified_data['weather'] = weather_summary
            logger.info("Successfully summarized weather data.")
            
        except (RequestException, HTTPError, ValueError) as e:
            # Catch API/Network errors from the client
            logger.error(f"Failed to fetch or process weather data: {e}")
            unified_data['error'] = f"Could not retrieve weather data. Details: {e.__class__.__name__}"
            return unified_data # Return immediately on failure
            
        # 2. Transform Data & Fetch Music Recommendation
        music_keyword = self._get_music_keyword(weather_raw)
        
        try:
            music_raw = self.music_client.fetch_data(music_keyword)
            
            # 3.3.3: Data Structure Validation for Music (check if results exist)
            music_results = music_raw.get('results', [])
            
            if music_results:
                # Select the first result as the recommendation
                best_match = music_results[0]
                music_summary = {
                    'title': best_match.get('collectionName', 'N/A'),
                    'artist': best_match.get('artistName', 'N/A'),
                    'genre': best_match.get('primaryGenreName', music_keyword),
                    'link': best_match.get('collectionViewUrl', 'N/A')
                }
                unified_data['recommendation'] = music_summary
                logger.info("Successfully fetched and summarized music recommendation.")
            else:
                unified_data['recommendation'] = f"No specific music found for '{music_keyword}'. Try another city."

        except (RequestException, HTTPError) as e:
            # Catch API/Network errors from the client
            logger.error(f"Failed to fetch or process music data: {e}")
            unified_data['recommendation'] = f"Music search failed. Details: {e.__class__.__name__}"

        return unified_data