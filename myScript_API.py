"""Testing web APIs with HTTP GET method"""

import json
import sys

import requests

headers = {
    'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
    'x-rapidapi-key': "baa5d585cdmshafe516d2f25baefp17cff6jsn73ac6fca864f"
}

def cityId(city_name):
    """Retrieve city ID from GeoDB API"""
    api_url = "http://geodb-free-service.wirefreethought.com/v1/geo/cities/"

    querystring = {"namePrefix": city_name}
    response = requests.get(api_url, headers=headers, params=querystring)
    try:
        cityData = json.loads(response.text)['data']
        cityId = cityData[0]['wikiDataId']
        return cityId
    except KeyError:
        print("Unknown city")


def city_details(city_name):
    """Retrieve city details from GeoDB API"""
    details_url = "http://geodb-free-service.wirefreethought.com/v1/geo/cities/"
    cityCode = cityId(city_name)
    try:
        details_url = details_url + str(cityCode)
        resp = requests.get(details_url, headers=headers)

        cityDetails = json.loads(resp.text)['data']
        print("Name: ", cityDetails['name'])
        print("Country: ", cityDetails['country'])
        print("Region: ", cityDetails['region'])
        print("Elevation de la ville: ", cityDetails['elevationMeters'])
        print("Latitude: ", cityDetails['latitude'])
        print("Longitude: ", cityDetails['longitude'])
        print("Population: ", cityDetails['population'])
        print("Time zone: ", cityDetails['timezone'])
    except KeyError:
        print("Unknown city")

def cities_around(city_name, radius):
    """Retrieve city around from GeoDB API"""
    url_first_part = "http://geodb-free-service.wirefreethought.com/v1/geo/cities/"
    querystring = {"radius": radius}
    cityCode = cityId(city_name)
    try:
        url_second_part = url_first_part + str(cityCode)
        around_url = url_second_part + "/nearbyCities"
        resp = requests.get(around_url, headers=headers, params=querystring)

        data_cities_around = json.loads(resp.text)['data']
        cities_around = []
        for i, cities in enumerate(data_cities_around):
            city_name = data_cities_around[i]['city']
            cities_around.append(city_name)
        print(*cities_around, sep = "\n")
    except KeyError:
        print("Unknown city")



if __name__ == "__main__":
    try:
        service = sys.argv[1]
        if service == "details":
            try:
                city_name = sys.argv[2]
                city_details(city_name)
            except IndexError:
                print("Please enter a city name")
        elif service == "around":
            try:
                city_name = sys.argv[2]
                if int(sys.argv[3]) > 0:
                    radius = sys.argv[3]
                else:
                    radius = 100
                cities_around(city_name, radius)
            except IndexError:
                print("Please enter a city name and radius (radius will be 100 if you enter nothing)")
        else:
            print("Unknown action, please enter 'details or 'around'")
    except IndexError:
        print("Missing action, please use either 'details' or 'around'")
