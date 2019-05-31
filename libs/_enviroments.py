import subprocess as sp

class Enviroments(object):
    """docstring for Enviroments."""

    flavor_elements = {
        0:'id:',
        1:'name:',
        2:'ram:',
        3:'disk:',
        4:'ephemeral:',
        5:'vcpu:',
        6:'is_public:',
    }

    image_elements = {
        0:'id',
        1:'name',
        2:'status',
    }

    sec_group_elements = {
        0:'id',
        1:'name',
        2:'desc',
        3:'project',
        4:'tag',
    }
    sec_group_list = []

    def __init__(self):
        del self.sec_group_list[:]
        print "\t[*]Enviroments init"

    def split_list(self, alist, wanted_parts=1):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                 for i in range(wanted_parts) ]

    def get_flavors(self):
        self.flavor_list = sp.check_output(['openstack', 'flavor', 'list', '--format', 'value']).replace('\n', ' ').split(' ')
        return self.split_list(self.flavor_list, len(self.flavor_list)/6 )

    def get_images(self):
        self.image_list = sp.check_output(['openstack', 'image', 'list', '--format', 'value']).replace('\n', ' ').split(' ')
        return self.split_list(self.image_list, len(self.image_list)/3 )

    def get_sec_group(self):
        self.temp = sp.check_output(['openstack', 'security', 'group', 'list', '--format', 'csv']).replace('\n', ',').replace('\"','').split(',')
        self.sec_group_list = self.split_list(self.temp, len(self.temp)/5 )[1:]

        return self.sec_group_list
