#!/usr/bin/python3
"""
Fabric script to distribute an archive to your web servers.
"""
from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Replace with your username
env.key_filename = 'my_ssh_private_key'  # Replace with your private key path

def do_pack():
    """
    Compress the contents of the web_static folder into a .tgz archive.
    """
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except:
        return None

def do_deploy(archive_path):
    """
    Distribute an archive to the web servers and update the symbolic link.
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_no_extension = archive_name.split(".")[0]
        remote_path = "/data/web_static/releases/{}/".format(archive_no_extension)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, remote_path))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}web_static/* {}".format(remote_path, remote_path))
        run("rm -rf {}web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))
        print("New version deployed!")
        return True
    except:
        return False

def deploy():
    """
    Deploy the web_static archive to the web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
