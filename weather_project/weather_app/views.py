from django.shortcuts import render
import requests
from datetime import datetime, timedelta

def convert_to_ist(timestamp):
    # Convert the UNIX timestamp to a datetime object
    utc_time = datetime.utcfromtimestamp(timestamp)
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    return ist_time.strftime('%H:%M')

def home(request):

    city = request.GET.get('city', 'Mumbai')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=53529b9c98d61da45cb30d365763d0c6'

    try:
        # Request to OpenWeatherMap API
        response = requests.get(url)
        
        # Successful request (status code 200)
        if response.status_code == 200:
            # Parsing the JSON response
            data = response.json()
            # Construct payload dictionary with relevant data
            payload = {'city': data['name'], 
                       'temperature': int(data['main']['temp'] - 273),
                       'pressure' : data['main']['pressure'],
                       'humidity' : data['main']['humidity'],
                       'weather': data['weather'][0]['main'],
                       
                       }
            sunrise = convert_to_ist(data['sys']['sunrise'])
            sunset = convert_to_ist(data['sys']['sunset'])
            payload['sunrise'] = sunrise
            payload['sunset'] = sunset
            print(payload)
        else:
            # If the request was not successful, print an error message
            print("Failed to fetch weather data. Status code:", response.status_code)
    except requests.RequestException as e:
        # If an error occurs during the request (e.g., network issues), print the error
        print("An error occurred during the request:", e)
        payload = {}

    return render(request, 'home.html', payload)
