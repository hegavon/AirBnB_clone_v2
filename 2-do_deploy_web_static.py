#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
from fabric.api import env, put, run
import os

env.hosts = ['xx-web-01', 'xx-web-02']  # Replace 'xx-web-01' and 'xx-web-02' with actual IP addresses
env.user = 'ubuntu'  # Replace 'ubuntu' with the appropriate SSH username
env.key_filename = '~/.ssh/my_ssh_private_key'  # Replace '~/.ssh/my_ssh_private_key' with the path to your SSH private key


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/' + archive_name.split('.')[0]
        
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, archive_folder))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(archive_folder))
        
        return True
    except Exception as e:
        print(e)
        return False
