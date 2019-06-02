from views import Views
v = Views()

from flask import Flask, flash, redirect, render_template, request, session, abort, Markup

import subprocess as sp

class SystemOverview(object):
    """docstring for SystemOverview."""

    def __init__(self):
        print "\t[*]SystemOverview init"

    def flavor_action(self, action, id):
        if action == 'delete':
            self.status = self.delete_flavor(id)
            return self.status
        else:
            return 'No work.'


    def delete_flavor(self, id):
        try:
            self.status = sp.check_output(['openstack', 'flavor', 'delete', id])
            return "flavor delete succecfully"
        except Exception as e:
            return "flavor delete unsuccecfully {0}".format(e)

    def create_flavor(self, flavor_name, ram, disk, empheral, vcpu, is_public):
        try:
            if is_public == 'True':
                self.status = sp.check_output(['openstack', 'flavor', 'create',
                                                '--ram', ram,
                                                '--disk', disk,
                                                '--ephemeral', empheral,
                                                '--vcpus', vcpu,
                                                '--public',
                                                flavor_name])
                return "flavor delete succecfully"

            else:
                self.status = sp.check_output(['openstack', 'flavor', 'create',
                                                '--ram', ram,
                                                '--disk', disk,
                                                '--ephemeral', empheral,
                                                '--vcpus', vcpu,
                                                '--private',
                                                flavor_name])
                return "flavor create succecfully"

        except Exception as e:
            return "flavor create unsuccecfully {0}".format(e)
