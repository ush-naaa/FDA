Simple Data Connector: Music by Weather

🌟 What This Program Does

This program is a connector that checks the weather in any city you choose and then suggests music that fits the mood.

It connects two different internet services (APIs) to get the final result:

Weather Service (OpenWeatherMap): Checks the temperature and condition (like "Rain" or "Clouds").

Music Service (iTunes Search): Finds albums and artists based on the mood from the weather.

📁 How the Project is Built

The most important files:

main.py: This is the file you run. It asks for the city and prints the final answer.

data_aggregator.py: This is the brain. It reads the weather and decides which music keyword to search for (e.g., "Rainy Day Jazz").

api_clients.py: This file has the specific instructions for talking to the Weather website and the Music website.

🛠️ How to Set Up (Install)

You must do these steps before you run the program for the first time.

1. Secret Key Setup

You need to tell the program your personal Weather API key.

You must have a file named .env in your main project folder.

In this .env file, you must put your secret key like this: OPENWEATHERMAP_API_KEY=your_actual_key_here.

2. Install Libraries

You need to use a special Python tool to install the necessary extra software.

# 1. Make sure your (venv) is active!
# 2. Run the install command:
pip install -r requirements.txt


▶️ How to Run the Program

You must always use the special run command below.

Run this command in your terminal. The program will then ask you to type the city name.

python -m fda_aggregator.main


Example Run (What you will see):

Enter city name: London
WEATHER: London is 9.76°C with broken clouds.
MUSIC: Recommended Album: Lo-Fi Chillhop Playlist by Various Artists (House). Link: [URL]
