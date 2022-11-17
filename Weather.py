import requests


def get_weather(city, token):
    try:
        f = open('app_settings.txt', 'r')
        data = f.read().split('\n')

        lang = data[0][6:]
        degree = data[1][6:]

        lat, lon = get_coords(city, token)
        if lat == lon == 'Error':
            raise Exception

        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units={degree}&lang={lang}')

        data = r.json()

        return data

    except Exception:
        return 'Error'


def get_coords(city, token):
    try:
        r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={token}')
        data = r.json()
        lat, lon = data[0]['lat'], data[0]['lon']
        return lat, lon

    except Exception:
        return 'Error', 'Error'

