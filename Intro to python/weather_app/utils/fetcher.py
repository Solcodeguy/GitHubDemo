import requests

def get_weather():
    # Fetches current temperature in New York
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.00&current_weather=true"
    response = requests.get(url).json()
    return response["current_weather"]["temperature"]
