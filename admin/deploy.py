import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import common as c


APP_TYPE = 'admin'
APP_REPO = 'app/admin'
NGINX_IMAGE = 'nginx:1.11.4-alpine'


def deploy_image(branch_name, hub, hub_user, hub_pass):
    c.deploy_image(branch_name, APP_REPO, NGINX_IMAGE, hub, hub_user,
                   hub_pass, APP_TYPE)