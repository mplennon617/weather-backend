# Part 1: https://medium.com/@david_shortman/write-a-dead-simple-web-app-fast-for-a-hackathon-part-one-a-flask-backend-4410dc15970d
# Part 2: https://dev.to/davidshortman/write-a-dead-simple-web-app-fast-for-a-hackathon-part-two-debug-and-deploy-927

import os

from flask import Flask
from pyowm import OWM
from flask import request

app = Flask(__name__)
#owm = OWM('488a6abd6fac90573c30ec1cad8b1136') # OWM API Key
owm = OWM(os.environ.get('OPEN_WEATHER_API_KEY')) # OWM API Key (From Environment)


@app.route('/')
def hello():
    return 'Hello there'

@app.route('/weather/<country>/<city>')
# Weather route.
# @param country - string representing the country that we want weather data from.
# @param city - string representing the city (within country) that we want weather data from.
def weather(country, city):
    weather_manager = owm.weather_manager()
    weather_at_place = weather_manager.weather_at_place(f'{city},{country}')
    temperature = weather_at_place.weather.temperature('celsius')

    weather_details = {
        'temp_celsius': temperature['temp'],
        'temp_kelvin': temperature['temp'] + 273
    }

    print(request.args.get('show_humidity'))

    if (request.args.get('show_humidity')):
        weather_details['humidity'] = weather_at_place.weather.humidity

    if (request.args.get('show_precipitation')):
        weather_details['precipitation_last_hour'] = weather_at_place.weather.rain['1h']

    return weather_details

# at bottom of app.py...
if __name__ == "__main__":
    # Run on localhost if we do not have a container.
    if os.environ.get('IS_CONTAINER') != 'true':
        app.run(debug=True)
    # Otherwise, deploy on the correct environment port.
    else:
        port = os.environ.get('PORT')
        if port == None:
            port = '5000'
        app.run(host=f'0.0.0.0:{port}')