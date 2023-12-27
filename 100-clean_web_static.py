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


def do_deploy(archive_path):
    """
    Deploys static files to server and archives
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Archives and deploys the static files to server
    """
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False


def do_clean(number=0):
    """
    Deletes out-of-date archives of the static files.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
