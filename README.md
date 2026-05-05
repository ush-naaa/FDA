# 🎵 Simple Data Connector: Music by Weather

## 🌟 What This Program Does

This program is a connector that checks the weather in any city you choose and then suggests music that fits the mood.

It connects two different internet services (APIs) to get the final result:

* **Weather Service (OpenWeatherMap):** Checks the temperature and condition (like *Rain* or *Clouds*).
* **Music Service (iTunes Search):** Finds albums and artists based on the mood from the weather.

---

## 📁 Project Structure

The most important files:

* **`main.py`**
  This is the file you run. It asks for the city and prints the final answer.

* **`data_aggregator.py`**
  This is the brain. It reads the weather and decides which music keyword to search for (e.g., *"Rainy Day Jazz"*).

* **`api_clients.py`**
  This file contains the instructions for communicating with the Weather API and the Music API.

---

## 🛠️ Setup Instructions

Follow these steps before running the program for the first time.

### 1️⃣ Secret Key Setup

You need to provide your personal Weather API key:

* Create a file named **`.env`** in your main project folder
* Add your API key like this:

```env
OPENWEATHERMAP_API_KEY=your_actual_key_here
```

---

### 2️⃣ Install Dependencies

Make sure your virtual environment is active, then run:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Program

Run the following command in your terminal:

```bash
python -m fda_aggregator.main
```

The program will then prompt you to enter a city name.

---

## 🧠 Summary

* Takes a **city name** as input
* Fetches **weather data**
* Converts weather into a **music mood**
* Suggests **songs/albums** based on that mood

---

✨ Enjoy discovering music based on the weather!
