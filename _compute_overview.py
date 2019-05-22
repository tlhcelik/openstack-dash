from views import Views
v = Views()

from flask import Flask, flash, redirect, render_template, request, session, abort, Markup

import subprocess as sp

class ComputeOverview(object):
    """docstring for ComputeOverview."""
    new_list = []
    new_list_2 = []
    new_list_3 = []

    def __init__(self):
        print "[*]ComputeOverview init"
        del self.new_list[:]
        del self.new_list_2[:]
        del self.new_list_3[:]

    def split_list(self, alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                 for i in range(wanted_parts) ]

    def get_instances(self):
        self.server_list = list( sp.check_output(['openstack', 'server', 'list', '-f', 'csv'])
                    .replace(',',' ')
                    .split() )

        for i in range(len(self.server_list)):
            if self.server_list[i] == '\"\"':
                self.new_list.append('No Value')
            else:
                self.new_list.append(self.server_list[i])

        for i in range(len(self.new_list)):
            self.new_list_2.append(self.new_list[i].replace('\"',''))

        self.new_list_3 = self.new_list_2[6:]
        self.count = len(self.new_list_3) / 6

        return self.split_list(self.new_list_3, self.count)

    def instance_action(self, action, name):
        if action == 'start':
            self.status = self.start_instance(name)

        elif action == 'suspend':
            self.status = self.suspend_instance(name)

        elif action == 'resume':
            self.status = self.resume_instance(name)

        elif action == 'terminate':
            self.status = self.terminate_instance(name)

        else:
            return "[!]Error. Wrong action."

    def start_instance(self, name):
        try:
            self.status = sp.check_output(['openstack', 'server', 'start', name])
            print "[*]Instance start succecfully"
            return 1
        except Exception as e:
            print e
            return 0

    def suspend_instance(self, name):
        try:
            self.status = sp.check_output(['openstack', 'server', 'suspend', name])
            print "[*]Instance suspend succecfully"
            return 1
        except Exception as e:
            print e
            return 0

    def resume_instance(self, name):
        try:
            self.status = sp.check_output(['openstack', 'server', 'resume', name])
            print "[*]Instance resume succecfully"
            return 1
        except Exception as e:
            print e
            return 0

    def terminate_instance(self, name):
        try:
            self.status = sp.check_output(['nova', 'delete', name])
            print "[*]Instance delete(terminate) succecfully"
            return 1
        except Exception as e:
            print e
            return 0

    def create_instance(self, name, counter, image_id, flavor_id, security_group_id):
        try:
            self.status = sp.check_output(['openstack', 'server', 'create',
                                            '--flavor', flavor_id,
                                            '--image', image_id,
                                            '--security-group', security_group_id,
                                            name])
            print "[*]Instance create succecfully"
            return 1
        except Exception as e:
            print e
            return 0
