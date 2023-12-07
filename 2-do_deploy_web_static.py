#!/usr/bin/python3
"""
Module to bundle up contents in tgz file
with Fabric
"""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


"""
The list of host servers
"""
env.hosts = ["18.206.202.212", "100.26.212.51"]


@runs_once
def do_pack():
    """
    Generates the tgz file
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    initial_time = datetime.now()
    result = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            initial_time.year,
            initial_time.month,
            initial_time.day,
            initial_time.hour,
            initial_time.minute,
            initial_time.second
            )
    try:
        print("Packaging web_static to {}".format(result))
        local("tar -cvzf {} web_static".format(result))
        file_size = os.stat(result).st_size
        print("web_static packed: {} -> {} Bytes".format(result, file_size))
    except Exception as e:
        print(e)
        result = None
    return result
