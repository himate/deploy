import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import common as c


APP_TYPE = 'customers'
APP_REPO = 'app/customers'


def build_image(branch_name, hub, hub_user, hub_pass, build_host, fab_root):
    c.build_branch(branch_name, APP_TYPE)
    c.build_image(branch_name, APP_TYPE, hub, APP_REPO, build_host,
                  hub_user, hub_pass, fab_root)
