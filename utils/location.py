import requests  # working with apis
import json  # working with json data


# Get City
def get_location():
    # using api get request to track ip address location
    url = "http://ipinfo.io/json"
    response = requests.get(url)
    # load data into dictionary
    data = json.loads(response.text)
    # return city
    return data['city']
