import requests
import json


# Get City
def get_location():
    url = "http://ipinfo.io/json"
    response = requests.get(url)
    data = json.loads(response.text)
    return data['city']

