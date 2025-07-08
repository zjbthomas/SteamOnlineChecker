import urllib.request
import json

import os
import sys

FILENAME = 'languages.txt'

def _fetch_wishlist(api_key, steam_id): #Steam ID is the 64bit one
    req_headers = {'User-Agent': 'Python script'}
    url = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/?key=" + api_key + "&steamid=" + steam_id + "&format=json"
    req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
    response = urllib.request.urlopen(req)
    content = response.read()
    data = json.loads(content.decode('utf8'))
    
    return [item["appid"] for item in data["response"]["items"]]

def _fetch_languages(steamids):
    with open(FILENAME, 'w') as f:
        for appid in steamids:
            req_headers = {'User-Agent': 'Python script'}
            url = "https://store.steampowered.com/api/appdetails?appids=" + str(appid) + "&l=english"
            req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
            response = urllib.request.urlopen(req)
            content = response.read()
            data = json.loads(content.decode('utf8'))

            if data[str(appid)]['success']:
                app_data = data[str(appid)]
                supported_languages = app_data["data"]["supported_languages"]

                f.write(f"{appid},{'Chinese' in supported_languages}\n")

def run_steam(api_key, steam_id):
    wishlist = _fetch_wishlist(api_key, steam_id)

    _fetch_languages(wishlist)

if __name__ == "__main__":
    run_steam(sys.argv[1], sys.argv[2])