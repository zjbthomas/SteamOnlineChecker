import urllib.request
import json

import sys
import time
import os

FILENAME = 'languages.txt'
EXPIRATION = 4 # weeks

def _fetch_wishlist(api_key, steam_id): #Steam ID is the 64bit one
    req_headers = {'User-Agent': 'Python script'}
    url = "https://api.steampowered.com/IWishlistService/GetWishlist/v1/?key=" + api_key + "&steamid=" + steam_id + "&format=json"
    req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
    response = urllib.request.urlopen(req)
    content = response.read()
    data = json.loads(content.decode('utf8'))
    
    return [item["appid"] for item in data["response"]["items"]]

def _fetch_languages(steamids, fout):
    for appid in steamids:
        time.sleep(1) # Pause for 1 second

        req_headers = {'User-Agent': 'Python script'}
        url = "https://steamspy.com/api.php?request=appdetails&appid=" + str(appid)
        req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
        response = urllib.request.urlopen(req)
        content = response.read()
        
        try:
            data = json.loads(content.decode('utf8'))
            fout.write(f"{appid},{'Chinese' in data['languages']},0\n")
        except:
            print(f"Error processing appid {appid}: {data}")

def _read_existing_games():
    existing_games_map = {}

    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as f:
            for line in f.readlines():
                line = line.strip()

                if line:
                    appid, supported, duration = line.split(',')
                    existing_games_map[int(appid)] = (supported, int(duration))

    return existing_games_map

def _check_expiration(existing_games):
    keep_games = []

    for appid, (_, duration) in existing_games.items():
        if duration < EXPIRATION:
            keep_games.append(appid)

    return keep_games

def run_steam(api_key, steam_id):
    existing_games = _read_existing_games()

    keep_games = _check_expiration(existing_games)

    fout = open(FILENAME, 'w')

    # write existing games that are not expired (add 1 day to duration)
    for appid in keep_games:
        fout.write(f"{appid},{existing_games[appid][0]},{existing_games[appid][1] + 1}\n")

    wishlist = _fetch_wishlist(api_key, steam_id)

    # filter out games that are not expired
    update_games = [appid for appid in wishlist if appid not in keep_games]

    _fetch_languages(update_games, fout)

    fout.close()

if __name__ == "__main__":
    run_steam(sys.argv[1], sys.argv[2])