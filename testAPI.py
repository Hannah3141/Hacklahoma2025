import requests
import json

def get_weather(latitude: float, longitude: float):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

results = get_weather(52.52, 13.41)
#wResults = results.read()
#wjResults = json.loads(results)
print(results)