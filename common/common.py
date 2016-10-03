from fabric.api import (sudo, put, local, run, settings)
from fabric.context_managers import (lcd, shell_env)

import re


BUILD_DIR = 'cur_build'


def docker_login(user, password, domain):
    sudo('docker login --username=%s --password=%s %s' % (user,
                                                          password,
                                                          domain))


def docker_logout(domain):
    sudo('docker logout %s' % (domain))


def build_branch(branch_name, app_type, release='1.3.3'):
    with lcd('apps/%s' % (app_type)), shell_env(PACKAGE_DIRS='../../packages'):
        local('meteor --release %s build ../../%s' % (release, BUILD_DIR))


def build_image(branch_name, app_type, hub, repo, build_host,
                hub_user, hub_pass, fab_root):
    branch_name = re.sub('origin/', '', branch_name)
    branch_name = re.sub(r'\W', '-', branch_name)

    with settings(host_string=build_host):
        docker_login(hub_user, hub_pass, hub)
        put('%s/%s/docker/Dockerfile' % (fab_root, app_type), 'Dockerfile')
        put('%s/%s.tar.gz' % (BUILD_DIR, app_type), 'app.tar.gz')
        with settings(warn_only=True):
            run('rm -rf app')
        run('mkdir -p app')
        run('tar -xf app.tar.gz -C app')
        sudo('docker build -t %s/%s:%s-SNAPSHOT .' % (hub, repo, branch_name))
        sudo('docker push %s/%s:%s-SNAPSHOT ' % (hub, repo, branch_name))


def deploy_image(branch_name, app_repo, nginx_image, hub, hub_user, hub_pass,
                 app_type, mongo_url, root_url, port='8080',
                 nginx_container_name='nginx'):
    branch_name = re.sub('origin/', '', branch_name)
    branch_name = re.sub(r'\W', '-', branch_name)
    app_image = '%s/%s:%s-SNAPSHOT' % (hub, app_repo, branch_name)

    docker_login(hub_user, hub_pass, hub)
    sudo('docker pull %s' % (app_image))
    sudo('docker pull %s' % (nginx_image))
    with settings(warn_only=True):
        sudo('docker rm -f %s' % (nginx_container_name))
        sudo('docker rm -f %s' % (app_type))
    sudo('docker run -d --name %s '
         '-v /opt/%s_settings.json:/config/settings.json '
         '-e "MONGO_URL=%s" '
         '-e "ROOT_URL=%s" '
         '-e "PORT=%s" '
         '-e "METEOR_SETTINGS=$(cat /opt/%s_settings.json)" '
         '%s' % (app_type, app_type, mongo_url, root_url, port, app_type,
                 app_image))
    sudo('docker run -d --name %s '
         '-v /opt/nginx/nginx.conf:/etc/nginx/nginx.conf '
         '-v /opt/nginx/sites-enabled:/etc/nginx/sites-enabled '
         '-v /opt/nginx/conf.d:/etc/nginx/conf.d '
         '-v /etc/letsencrypt:/etc/letsencrypt '
         '-v nginx-logs:/var/log/nginx '
         '-p 443:443 '
         '-p 80:80 --link %s %s' % (nginx_container_name,
                                    app_type, nginx_image))
