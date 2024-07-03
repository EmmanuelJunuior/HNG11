import requests
from django.http import JsonResponse
from django.conf import settings

def hello(request):
    visitor = request.GET.get('visitor', 'Mark')

    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    
    ip_lookup_url = f"http://api.weatherapi.com/v1/ip.json?key={settings.WEATHER_API_KEY}&q={client_ip}"

    ip_response = requests.get(ip_lookup_url)
    ip_data = ip_response.json()

    if ip_response.status_code == 200:
        location = ip_data.get('city', 'Unknown')
    else:
        location = 'Unknown'
        print(f"location unknown")

    weather_url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={location}"

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if weather_response.status_code == 200:
        temp_c = weather_data['current']['temp_c']
        greeting = f"Hello, {visitor}!, the temperature is {temp_c} degrees Celsius in {location}"
    else:
        temp_c = 'N/A'
        greeting = f"Hello, {visitor}!, Request Error {location}"

    
    hello = {
        'client_ip': client_ip,
        'location': location,
        'greeting': greeting
    }

    return JsonResponse(hello)