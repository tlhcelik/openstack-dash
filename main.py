"""
LISENCED WITH GNU AFFERO GENERAL PUBLIC LICENSE (AGPLv3)

Created by Talha Celik
github.com/tlhcelik

"""


from flask import Flask, flash, redirect, render_template, request, session, abort, Markup

import os
import random

from views import Views
v = Views()

#page classes, each page have a class. (exp: _page-name.py)
from _settings import Settings
from _compute_overview import ComputeOverview
from _quotas import Quotas
from _enviroments import Enviroments

#globals
NOTIFY = 'All clear'

app = Flask(__name__)

@app.route('/settings')
def settings():
    settings_page = Settings()
    some_value = settings_page.do_it_some_transaction()
    return render_template(v._views['settings'],
                            some_value = some_value,

                        )

@app.route('/activity-logs')
def activity_logs():
    return render_template(v._views['activity-logs'])

@app.route('/blank')
def blank():
    return render_template(v._views['blank'])

################################################################################
# login definitions start
################################################################################

@app.route('/')
@app.route('/login')
def index():
    return render_template('login/login.html')

@app.route('/logout')
def logout():
    return index()

@app.route('/index', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    quotas_list = Quotas()
    quotas = quotas_list.get_quotas()
    print quotas
    return render_template('index.html',
                            random_num = random.randint(1,100),
                            running_instances = random.randint(1,10),
                            volume_storage = random.randint(1,550),
                            ram_status = random.randint(1,100),
                            quotas = quotas,
                        )

@app.route('/login/register')
def register():
    return render_template('login/register.html')

@app.route('/login/forgot-password')
def forgot_password():
    return render_template('login/forgot-password.html')

################################################################################
# login definitions end
################################################################################

################################################################################
# compute definitions start
################################################################################

@app.route('/compute/create-instance', methods=['POST', 'GET'])
def create_instance():
    global NOTIFY
    compute_overview_page = ComputeOverview()

    instance_name       = request.args.get('instance_name')
    counter             = request.args.get('counter')
    image_id            = request.args.get('image_id')
    flavor_id           = request.args.get('flavor_id')
    security_group_id   = request.args.get('security_group_id')

    status = compute_overview_page.create_instance(instance_name,
                                                    counter,
                                                    image_id,
                                                    flavor_id,
                                                    security_group_id
                                                    )

    NOTIFY = status
    return compute_overview()

@app.route('/<action>/<instance_name>')
def instance_transactions(action, instance_name):
    global NOTIFY
    compute_overview_page = ComputeOverview()
    status = compute_overview_page.instance_action(action, instance_name)
    NOTIFY = status

    return compute_overview()

@app.route('/compute/overview')
def compute_overview():
    global NOTIFY
    status = NOTIFY

    compute_overview_page = ComputeOverview()
    instance_values = compute_overview_page.get_instances()

    return render_template('compute/overview.html',
                            compute_collapse_status = "show",
                            overview_status     = "active",
                            page_location       = "/compute/overview",
                            page_name           = "Home > Compute > Overview",
                            notify              = status,
                            instance_values     = instance_values,
                            instance_count      = len(instance_values),
                            )

@app.route('/compute/test')
def compute_test():
    enviroments = Enviroments()

    sec_group = enviroments.get_sec_group()

    return "TEST ENDED"

@app.route('/compute/instances')
def compute_instances():
    quotas_list = Quotas()
    quotas = quotas_list.get_quotas()

    enviroments = Enviroments()
    flavors = enviroments.get_flavors()
    images = enviroments.get_images()
    sec_groups = enviroments.get_sec_group()

    return render_template('compute/instances.html',
                            page_name               = "Home > Compute > Instances",
                            instances_status        = "active",
                            compute_collapse_status = "show",
                            page_location           = "/compute/instances",
                            quotas                  = quotas,
                            flavors                 = flavors,
                            images                  = images,
                            sec_groups              = sec_groups,
                            )

@app.route('/compute/api-access')
def compute_access():
    return render_template('compute/api-access.html',
                            api_access_status="active",
                            compute_collapse_status="show",
                            page_location = "/compute/api-access",
                            page_name = "Home > Compute > API Access",
                            )

@app.route('/compute/images')
def compute_images():
    return render_template('compute/images.html',
                            images_status="active",
                            compute_collapse_status="show",
                            page_location = "/compute/images",
                            page_name = "Home > Compute > Images"
                            )

@app.route('/compute/volumes')
def compute_volumes():
    return render_template('compute/volumes.html',
                            volumes_status="active",
                            compute_collapse_status="show",
                            page_location = "/compute/volumes",
                            page_name = "Home > Compute > Volumes"
                            )

@app.route('/compute/keypairs')
def compute_keypairs():
    return render_template('compute/keypairs.html',
                            keypairs_status="active",
                            compute_collapse_status="show",
                            page_location = "/compute/keypairs",
                            page_name = "Home > Compute > Keypairs"
                            )

################################################################################
# compute definitions end
################################################################################

################################################################################
# network definitions start
################################################################################

@app.route('/network/networks')
def network_networks():
    return render_template('network/networks.html',
                            networks_status="active",
                            network_collapse_status="show",
                            page_location = "/network/networks",
                            page_name = "Home > Network > Networks"
                            )

@app.route('/network/routers')
def network_routers():
    return render_template('network/routers.html',
                            routers_status="active",
                            network_collapse_status="show",
                            page_location = "/network/routers",
                            page_name = "Home > Network > routers"
                            )

@app.route('/network/security-groups')
def network_security_groups():
    return render_template('network/security-groups.html',
                            security_groups_status="active",
                            network_collapse_status="show",
                            page_location = "/network/networks",
                            page_name = "Home > Network > Security Groups"
                            )

@app.route('/network/floating-ips')
def network_floating_ips():
    return render_template('network/floating-ips.html',
                            floating_ips_status="active",
                            network_collapse_status="show",
                            page_location = "/network/floating-ips",
                            page_name = "Home > Network > Floating IPs"
                            )

################################################################################
# object storage definitions start
################################################################################

@app.route('/storage/containers')
def storage_containers():
    return render_template('storage/containers.html',
                            containers_status="active",
                            storage_collapse_status="show",
                            page_location = "/storage/containers",
                            page_name = "Home > Storage > Containers"
                            )

################################################################################
# object storage definitions end
################################################################################

################################################################################
# system definitions start
################################################################################

@app.route('/system/overview')
def system_overview():
    return render_template('system/overview.html',
                            overview_status="active",
                            system_collapse_status="show",
                            page_location = "/system/overview",
                            page_name = "Home > System > Overview"
                            )

@app.route('/system/hypervisors')
def system_hypervisors():
    return render_template('system/hypervisors.html',
                            hypervisors_status="active",
                            system_collapse_status="show",
                            page_location = "/system/hypervisors",
                            page_name = "Home > System > Hypervisors"
                            )

@app.route('/system/host-aggregates')
def system_host_aggregates():
    return render_template('system/host-aggregates.html',
                            host_aggregates_status="active",
                            system_collapse_status="show",
                            page_location = "/system/host-aggregates",
                            page_name = "Home > System > Host Aggregates"
                            )

@app.route('/system/instances')
def system_instances():
    return render_template('system/instances.html',
                            instances_status="active",
                            system_collapse_status="show",
                            page_location = "/system/instances",
                            page_name = "Home > System > Instances"
                            )
@app.route('/system/volumes')
def volumes():
    return render_template('system/volumes.html',
                            volumes_status="active",
                            system_collapse_status="show",
                            page_location = "/system/volumes",
                            page_name = "Home > System > Volumes"
                            )

@app.route('/system/flavors')
def system_flavors():
    return render_template('system/flavors.html',
                            flavors_status="active",
                            system_collapse_status="show",
                            page_location = "/system/flavors",
                            page_name = "Home > System > Flavors"
                            )

@app.route('/system/images')
def system_images():
    return render_template('system/images.html',
                            images_status="active",
                            system_collapse_status="show",
                            page_location = "/system/images",
                            page_name = "Home > System > Images"
                            )

@app.route('/system/routers')
def system_routers():
    return render_template('system/routers.html',
                            routers_status="active",
                            system_collapse_status="show",
                            page_location = "/system/routers",
                            page_name = "Home > System > Routers"
                            )

@app.route('/system/floating-ips')
def system_floating_ips():
    return render_template('system/floating-ips.html',
                            floating_ips_status="active",
                            system_collapse_status="show",
                            page_location = "/system/floating-ips",
                            page_name = "Home > System > Floating IPs"
                            )
@app.route('/system/defaults')
def system_defaults():
    return render_template('system/defaults.html',
                            defaults_status="active",
                            system_collapse_status="show",
                            page_location = "/system/defaults",
                            page_name = "Home > System > Defaults"
                            )


@app.route('/system/metadata')
def system_metadata():
    return render_template('system/metadata.html',
                            metadata_status="active",
                            system_collapse_status="show",
                            page_location = "/system/metadata",
                            page_name = "Home > System > Metadata"
                            )

@app.route('/system/sys-info')
def system_sys_info():
    return render_template('system/sys-info.html',
                            sys_info_status="active",
                            system_collapse_status="show",
                            page_location = "/system/sys-info",
                            page_name = "Home > System > System Information"
                            )

################################################################################
# system storage definitions start
################################################################################

################################################################################
# profile definitions start
################################################################################

@app.route('/profile/projects')
def profile_projects():
    return render_template('profile/projects.html',
                            projects_status="active",
                            profiles_collapse_status="show"
                            )

@app.route('/profile/users')
def profile_users():
    return render_template('profile/users.html',
                            users_status="active",
                            profiles_collapse_status="show"
                            )

@app.route('/profile/groups')
def profile_groups():
    return render_template('profile/groups.html',
                            groups_status="active",
                            profiles_collapse_status="show"
                            )

@app.route('/profile/roles')
def profile_roles():
    return render_template('profile/roles.html',
                            roles_status="active",
                            profiles_collapse_status="show"
                            )

################################################################################
# profile definitions start
################################################################################

################################################################################
# run dashboard in local openstack installed machine
# python main.py
################################################################################
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=1158)
