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
