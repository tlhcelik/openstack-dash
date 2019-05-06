from views import Views
v = Views()

from flask import Flask, flash, redirect, render_template, request, session, abort, Markup

import subprocess as sp




class ComputeOverview(object):
    """docstring for ComputeOverview."""

    def __init__(self):
        print "ComputeOverview init"

    def get_instances(self):
        self.x = sp.check_output(['openstack', 'server', 'list', '-f', 'csv'])
        self.y = self.x.replace(',',' ')
        self.z = list(self.y.split())
        return self.z[6:12]
