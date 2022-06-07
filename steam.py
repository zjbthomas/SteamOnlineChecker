import urllib.request
import json

import os
import sys

def _is_online(api_key, steam_id): #Steam ID is the 64bit one
    req_headers = {'User-Agent': 'Python script'}
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + api_key + "&steamids=" + steam_id + "&format=json"
    req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
    response = urllib.request.urlopen(req)
    content = response.read()
    data = json.loads(content.decode('utf8'))
    if data["response"]["players"][0]["personastate"] != 0:
        return True 
    else:
        return False

def _create_msg(is_online):
    if (is_online):
        return ''
    else:
        return 'Steam not online! '

def run_steam(api_key, steam_id):
    is_online = _is_online(api_key, steam_id)
    return _create_msg(is_online)

if __name__ == "__main__":
    print(run_steam(sys.argv[1], sys.argv[2]))