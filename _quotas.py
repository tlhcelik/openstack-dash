import subprocess as sp



class Quotas(object):
    """docstring for Quotas."""

    new_list = [
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
    new_list_3 = []
    def __init__(self):
        print "Quotas init"


    def get_quotas(self):

        self.x = sp.check_output(['openstack', 'quota', 'show', '--default', '--format', 'yaml']).split()

        for i in range(len(self.new_list)):
            for j in range(len(self.x)):
                if self.x[j] == self.new_list[i]:
                    self.new_list_2.append(self.x[j+1])


        return self.new_list_2
