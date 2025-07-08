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
    req_headers = {'User-Agent': 'Python script'}
    url = "https://store.steampowered.com/api/appdetails?appids=" + steamids + "&l=english"
    req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
    response = urllib.request.urlopen(req)
    content = response.read()
    data = json.loads(content.decode('utf8'))
    
    return data

def _check_supported_languages(wishlist, languages):
    with open(FILENAME, 'w') as f:
        for appid in wishlist:
            appid = str(appid)  # Ensure appid is a string for dictionary lookup
            if appid in languages:
                app_data = languages[appid]
                if ("data" in app_data):
                    supported_languages = app_data["data"]["supported_languages"]

                    f.write(f"{appid},{"Chinese" in supported_languages}\n")
    
def run_steam(api_key, steam_id):
    wishlist = _fetch_wishlist(api_key, steam_id)
    languages = _fetch_languages(",".join(map(str, wishlist)))

    _check_supported_languages(wishlist, languages)

if __name__ == "__main__":
    run_steam(sys.argv[1], sys.argv[2])