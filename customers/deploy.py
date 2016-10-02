import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import common as c


APP_TYPE = 'customers'
APP_REPO = 'app/customers'
NGINX_IMAGE = 'nginx:1.11.4-alpine'


def deploy_image(branch_name, hub, hub_user, hub_pass, mongo_url, root_url):
    c.deploy_image(branch_name, APP_REPO, NGINX_IMAGE, hub, hub_user,
                   hub_pass, APP_TYPE, mongo_url, root_url)
