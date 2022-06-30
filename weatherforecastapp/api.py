import requests
from weatherforecast.settings import API_key

def kelvin_to_celsius_conv(kelvin_temp):
    celsius_temp = float(kelvin_temp) - 273.15
    return round(celsius_temp, 1)


def coordinates_fun(city_name, limit):
    response = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API_key}')

    if response.status_code != requests.codes.ok:
        return "Something went terribly wrong!"
    else:
        results = response.json()[0]
        coordinates = (results["lat"], results["lon"])
        return coordinates


def get_weather_data(coordinates):
    # global response
    response = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates[0]}&lon={coordinates[1]}&appid={API_key}")

    if response.status_code != requests.codes.ok:
        print("Something went terribly wrong!")
    else:
        return response