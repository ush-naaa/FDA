import sys
# Import DataAggregator and configuration
from fda_aggregator.config import load_config
from fda_aggregator.data_aggregator import DataAggregator
from requests.exceptions import RequestException

def run_fda():
    """The main entry point of the application. Handles user input and displays results."""
    
    # 3.2. Secure Configuration Management
    load_config()

    try:
        # Get city from command line argument or user input
        city = ""
        if len(sys.argv) < 2:
            # Prompt the user directly for the city if no argument is provided
            city = input("Enter city name: ")
        else:
            city = sys.argv[1]
            
        if not city:
            # If the user enters an empty city name when prompted
            print("ERROR: City name is required.")
            return

        # Instantiate the core aggregation class
        aggregator = DataAggregator()
        
        # Run the aggregation logic
        result = aggregator.get_recommendation(city)

        # --- Prettier Output Display ---
        
        if 'error' in result:
             # If a major error occurred (e.g., API key missing, bad city name)
             print(f"FATAL ERROR: {result['error']}")
             return
        
        # 1. Display Weather Summary
        w = result.get('weather', {})
        print("\n--- ☀️  WEATHER SUMMARY ---")
        print(f"  • City: {w.get('city', city)}")
        print(f"  • Temperature: {w.get('temperature_c', 'N/A')}°C")
        print(f"  • Condition: {w.get('condition', 'N/A').title()}")
        
        # 2. Display Music Recommendation
        r = result.get('recommendation')
        if isinstance(r, dict):
            print("\n--- 🎧 MUSIC RECOMMENDATION ---")
            print(f"  • Album: {r['title']}")
            print(f"  • Artist: {r['artist']}")
            print(f"  • Genre: {r['genre']}")
            print(f"  • Link: {r['link']}")
        else:
            print("\n--- 🎧 MUSIC RECOMMENDATION ---")
            print(f"  • Message: {r}")


    except ValueError as e:
        # Catches the ValueError raised if the OPENWEATHERMAP_API_KEY is missing
        print(f"CONFIG ERROR: {e}")
    except RequestException as e:
        # Catches a general network failure that might happen before or during API client instantiation
        print(f"NETWORK ERROR: Could not connect to API during startup ({e.__class__.__name__})")
    except Exception as e:
        # Catch any unexpected top-level errors
        print(f"UNHANDLED ERROR: {e}")

if __name__ == "__main__":
    run_fda()