import requests

# URL = "https://geocode.search.hereapi.com/v1/geocode"
# #location = input("Enter the location here: ") #taking user input
# api_key = 'ODfYgIX45wrL41qboC3F_z2hg8e5_ABJYi71Pu6o948' # Acquire from developer.here.com
# PARAMS = {'apikey':api_key,'q':location} 

def get_location(url, params):
    # sending get request and saving the response as response object 
    r = requests.get(url, params) 
    data = r.json()

    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']

    loc = [latitude, longitude]

    return loc



