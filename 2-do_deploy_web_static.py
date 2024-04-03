#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import *
from os.path import exists
from fabric.exceptions import NetworkError

env.hosts = ['54.160.73.250', '52.90.22.193']
env.user = 'ubuntu'
env.key_filename = ['my_ssh_private_key']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    foldername = filename.split('.')[0]

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}/'.format(foldername))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(filename, foldername))
        run('rm /tmp/{}'.format(filename))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'
            .format(foldername, foldername))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(foldername))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(foldername))
        print("New version deployed!")
        return True
    except NetworkError as e:
        print("Error: Network issue occurred - {}".format(e))
        return False
    except Exception as e:
        print("Error: An unexpected error occurred - {}".format(e))
        return False
