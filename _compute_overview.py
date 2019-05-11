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
        print "ComputeOverview init"

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

        del self.new_list[:]
        del self.new_list_2[:]

        return self.split_list(self.new_list_3, self.count)
