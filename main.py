import requests

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"
API_KEY = "6c8b4d4bf2b5451da07180440251601"
days = 5


print("\t\t***Weather App***")
city = input("Enter the City/State/Country Name: ")
response = requests.get(BASE_URL, params={
    "key": API_KEY,
    "q": city,
    "days": days
})

if response.status_code == 200:
    data = response.json()
    city = data['location']['name']
    forecast = data['forecast']['forecastday']
    print(f"City: {city}")
    print("Forecast:")
    for day in forecast:
        date = day['date']
        condition = day['day']['condition']['text']
        temp = day['day']['avgtemp_c']
        print(f"{date}: {condition}, avg_temp: {temp}")
else:
    print(f"Error: No city found.")
