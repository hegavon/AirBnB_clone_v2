#!/usr/bin/env python3
"""
Fabric script to generate a .tgz archive from the contents of the web_static folder
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    time = datetime.now()
    archive_name = 'web_static_{}.tgz'.format(time.strftime('%Y%m%d%H%M%S'))
    local('mkdir -p versions')
    result = local('tar -cvzf versions/{} web_static'.format(archive_name))
    if result.succeeded:
        return 'versions/{}'.format(archive_name)
    else:
        return None
