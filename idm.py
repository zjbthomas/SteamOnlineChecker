import os
import re
import urllib.request
import json
from bs4 import BeautifulSoup

FILENAME = 'history.txt'

def _get_latest():
    url = "https://lrepacks.net/repaki-programm-dlya-interneta/56-internet-download-manager-repack.html"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    bs = BeautifulSoup(response,"html.parser")

    title = bs.find("title").text
    x = re.search("Internet Download Manager ([0-9\.]+)", title)

    if (x):
        return x.group(1)
    else:
        return None

def _create_msg(version):
    updated = False

    # read file to get last version
    if (version is None):
        updated = True
    else:
        if os.path.exists(FILENAME):
            with open(FILENAME, 'r') as f:
                content = f.read().strip()

                if (content != version):
                    updated = True
        else:
            updated = True

    # write latest version
    with open(FILENAME, 'w') as f:
        f.write(version)

    # update env
    if (updated):
        return 'IDM updated to ' + version + '! '
    else:
        return ''

def run_idm():
    version = _get_latest()
    return _create_msg(version)

if __name__ == "__main__":
    print(run_idm())