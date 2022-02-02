import urllib.request
import json
import sys

import os

def _is_online(api_key, steam_id): #Steam ID is the 64bit one
    req_headers = {'User-Agent': 'Python script'}
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + api_key + "&steamids=" + steam_id + "&format=json"
    req = urllib.request.Request(url, data=None, headers=req_headers, origin_req_host=None)
    response = urllib.request.urlopen(req)
    content = response.read()
    data = json.loads(content.decode('utf8'))
    if data["response"]["players"][0]["personastate"] == 1:
        return True 
    else:
        return False

def _update_env(is_online):
    env_file = os.getenv('GITHUB_ENV')

    with open(env_file, "w") as f:
        if (is_online):
            f.write("notification=false")
        else:
            f.write("notification=true")

def main(api_key, steam_id):
    is_online = _is_online(api_key, steam_id)
    _update_env(is_online)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])