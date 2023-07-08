#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import *
import os
env.hosts = ['54.172.102.75', '54.160.119.245']


def do_deploy(archive_path):
    """Archive distributor"""
    try:
        try:
            if os.path.exists(archive_path):
                arc_tgz = archive_path.split("/")
                arg_save = arc_tgz[1]
                arc_tgz = arc_tgz[1].split('.')
                arc_tgz = arc_tgz[0]

                """Upload archive to the server"""
                put(archive_path, '/tmp')

                """Save folder paths in variables"""
                uncomp_fold = '/data/web_static/releases/{}'.format(arc_tgz)
                tmp_location = '/tmp/{}'.format(arg_save)

                """Run remote commands on the server"""
                run('mkdir -p {}'.format(uncomp_fold))
                run('tar -xvzf {} -C {}'.format(tmp_location, uncomp_fold))
                run('rm {}'.format(tmp_location))
                run('mv {}/web_static/* {}'.format(uncomp_fold, uncomp_fold))
                run('rm -rf {}/web_static'.format(uncomp_fold))
                run('rm -rf /data/web_static/current')
                run('ln -sf {} /data/web_static/current'.format(uncomp_fold))
                run('sudo service nginx restart')
                return True
            else:
                print('File does not exist')
                return False
        except Exception as err:
            print(err)
            return False
    except Exception:
        print('Error')
        return False
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
