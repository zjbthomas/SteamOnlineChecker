import sys
import os

from steam import run_steam
from idm import run_idm

def _update_env(msg_steam, msg_idm):
    flag = (msg_steam is not '') or (msg_idm is not '')

    msg = msg_steam + msg_idm

    env_file = os.getenv('GITHUB_ENV')

    with open(env_file, "w") as f:
        if (flag):
            f.write("notification=true\n")
            f.write("msg=" + msg + "\n")
        else:
            f.write("notification=false\n")
            
if __name__ == "__main__":
    _update_env(run_steam(sys.argv[1], sys.argv[2]), run_idm())