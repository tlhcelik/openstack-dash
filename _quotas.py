import subprocess as sp


from _compute_overview import ComputeOverview
from _enviroments import Enviroments

class Quotas(object):
    """docstring for Quotas."""

    maximum_quotas_values = [
        'cores:',
        'ram:',
        'instances:',
        'volumes:',
        'networks:',
        'floating_ips:',
        'snapshots:',
        'secgroups:',
        'routers:',
        'project_name',
        'subnets',
    ]

    new_list_2 = []
    instance_flavor_list = []
    total_using_ram = 0

    def __init__(self):
        del self.new_list_2[:]
        print "\t[*]Quotas init"


    def get_quotas(self):
        """
        1. get instaces
        2. get this instaces flavors
        3. get each one flavors ram
        4. calculate total using ram
        """
        self.x = sp.check_output(['openstack', 'quota', 'show', '--default', '--format', 'yaml']).split()

        for i in range(len(self.maximum_quotas_values)):
            for j in range(len(self.x)):
                if self.x[j] == self.maximum_quotas_values[i]:
                    self.new_list_2.append(self.x[j+1])


        return self.new_list_2

    def get_current_using(self, type = None):
        self.compute_overview = ComputeOverview()
        self.instances = self.compute_overview.get_instances()
        for i in range(len(self.instances)):
            self.instance_flavor_list.append(self.instances[i][5])

        self.flavor = Enviroments()
        self.flavors = self.flavor.get_flavors()

        for i in range(len(self.flavors)):
            for using_flavor in self.instance_flavor_list:
                if (self.flavors[i][1] == using_flavor):
                    self.total_using_ram += int(self.flavors[i][2])
        if type == 'ram':
            return self.total_using_ram
        else:
            return 0
