#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

from fabric.api import *
from os.path import exists

env.hosts = ['54.160.73.250', '52.90.22.193']
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    from datetime import datetime
    time = datetime.now()
    archive_name = 'versions/web_static_{}.tgz'.format(
        time.strftime('%Y%m%d%H%M%S'))
    local('mkdir -p versions')
    result = local('tar -cvzf {} web_static'.format(archive_name))
    if result.succeeded:
        return archive_name
    else:
        return None


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
    except Exception as e:
        print("Error: {}".format(e))
        return False


def deploy():
    """
    Deploys the latest version of web_static
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
