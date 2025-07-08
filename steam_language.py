import urllib.request
import json

import sys
import time

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
            time.sleep(1) # Pause for 1 second

            req_headers = {'User-Agent': 'Python script'}
            url = "https://steamspy.com/api.php?request=appdetails&appid=" + str(appid)
            req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
            response = urllib.request.urlopen(req)
            content = response.read()
            
            try:
                data = json.loads(content.decode('utf8'))
                f.write(f"{appid},{'Chinese' in data['languages']}\n")
            except:
                print(f"Error processing appid {appid}: {data}")

def run_steam(api_key, steam_id):
    wishlist = _fetch_wishlist(api_key, steam_id)

    _fetch_languages(wishlist)

if __name__ == "__main__":
    run_steam(sys.argv[1], sys.argv[2])