import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import common as c


APP_TYPE = 'admin'
APP_REPO = 'app/admin'


def build_image(branch_name, hub, hub_user, hub_pass):
    c.build_branch(branch_name, APP_TYPE)
    c.docker_login(hub_user, hub_pass, hub)
    c.build_image(branch_name, APP_TYPE, hub, APP_REPO)
