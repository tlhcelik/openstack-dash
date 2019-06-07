from pymongo import MongoClient
from _compute_overview import ComputeOverview

class Database(object):
    """docstring for Database."""

    value_list = []
    db_instance = {}

    def __init__(self, db_name, collection):
        print '\t[*]Database init'
        try:
            self.client = MongoClient("mongodb://user0:user0-pass@mongodb-cluster0-shard-00-00-tuftj.mongodb.net:27017,mongodb-cluster0-shard-00-01-tuftj.mongodb.net:27017,mongodb-cluster0-shard-00-02-tuftj.mongodb.net:27017/test?ssl=true&replicaSet=mongodb-cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
            self.db = self.client.get_database(db_name)
            self.collection = self.db[collection]

        except Exception as e:
            return 'Cannot connect MongoDB ' + str(e)
        finally:
            del self.value_list[:]
            self.db_instance.clear()

    def get_collection(self, collection):
        '''
        get all instance vales
        Example value_list eleman for instance: value_list[0]['name']
        '''
        self.values =  self.collection.find({})

        for instance in self.values:
           self.value_list.append(instance)

        return self.value_list, self.values.count()

    def check_doc_for_instances(self):
        self.db_instance_list, self.doc_count = self.get_collection(collection = 'instances')

        self.compute_overview = ComputeOverview()
        self.openstack_instances = self.compute_overview.get_instances()

        # no instance on openstack and db
        if self.doc_count == 0 and len(self.openstack_instances) == 0:
            print '\t[*]DB was updated'
        else:
            print '\t[*]DB updating...'
            for i in range(0, len(self.openstack_instances)):
                if self.doc_count != 0:
                    if self.db_instance_list[i]['id'] != self.openstack_instances[i][0]:
                        self.db_instance.update({
                                            'id':  self.openstack_instances[i][0],
                                            'name': self.openstack_instances[i][1],
                                            'status': self.openstack_instances[i][2],
                                            'network-provider': self.openstack_instances[i][3],
                                            'image': self.openstack_instances[i][4],
                                            'flavor': self.openstack_instances[i][5],
                                            })

                        self.is_add_db = self.collection.insert_one(self.db_instance)
                        self.db_instance.clear()
                        print '\t[*]DB updated'
                else:
                    self.db_instance.update({
                                        'id':  self.openstack_instances[i][0],
                                        'name': self.openstack_instances[i][1],
                                        'status': self.openstack_instances[i][2],
                                        'network-provider': self.openstack_instances[i][3],
                                        'image': self.openstack_instances[i][4],
                                        'flavor': self.openstack_instances[i][5],
                                        })
                    #print self.db_instance
                    self.is_add_db = self.collection.insert_one(self.db_instance)
                    self.db_instance.clear()
                    print '\t[*]DB updated'
        return 'OK'

        def delete_selected_instance(instance_name = 0):
            self.collection.delete_one({'name': instance_name})
        pass
