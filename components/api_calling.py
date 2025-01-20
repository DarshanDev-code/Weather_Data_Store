import requests

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"
API_KEY = "6c8b4d4bf2b5451da07180440251601"
days = 3

def get_whether_forecast(city):
    try:
        response = requests.get(BASE_URL, params={
            "key": API_KEY,
            "q": city,
            "days": days
        })
        response.raise_for_status()
        return {
            'success': True,
            'data': response.json()}
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'msg': f'Failed to fetch data . Reason: {e}'
        }

