#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents 
    of the web_static folder using the do_pack
"""

from fabric.api import local
from os.path import isdir
from datetime import datetime


def do_pack():
    """ Generate a .tgz archive file from the contents in web_static """
    date = datatime.now().strftime("%Y%m%d%H%M%S")
    try:
        #check if the versions exits
        if isdir("versions") is False:
            local("mkdir versions")
        file_path = "versions/web_static_{}.tgz".format(date)
        local("tar -czvf {} web_static".format(file_path))
        return file_name
    except:
        return None
