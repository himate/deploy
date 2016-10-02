from fabric.api import (sudo, put, local, run)
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


def build_image(branch_name, app_type, hub, repo):
    branch_name = re.sub('origin/', '', branch_name)
    branch_name = re.sub(r'\W', '-', branch_name)

    put('%s/docker/Dockerfile' % (app_type), 'Dockerfile')
    put('%s/%s.tar.gz' % (BUILD_DIR, app_type), 'app.tar.gz')
    run('rm -rf app')
    run('mkdir -p app')
    run('tar -xf app.tar.gz -C app')
    sudo('docker build -t %s/%s:%s-SNAPSHOT .' % (hub, repo, branch_name))
    sudo('docker push %s/%s:%s-SNAPSHOT ' % (hub, repo, branch_name))
