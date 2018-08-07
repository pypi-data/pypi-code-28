#!/usr/env/python3

import os
import yaml
import pprint
import getpass

global cf

default_config = '''--- # YAML Camoco Configuration File
options:
    basedir: ~/.minus80/

cloud:
    endpoint: https://s3.msi.umn.edu
    access_key: None
    secret_key: None

'''.format(**{'user':getpass.getuser()})

class Level(dict):
    '''
        Ha! Take that config parser! I am accessing
        everything like an object.
    '''
    def __init__(self,*args,**kwargs):
        # Create the dict
        super().__init__(*args,**kwargs)
        # Convert to Levels

        for k,v in self.items():
            if isinstance(v,dict):
                self[k] = Level(v)
            else:
                self[k] = v

    def __getattr__(self,item):
        if 'dir' in item and '~' in self[item]:
            return os.path.expanduser(self[item])
        return self[item]
    def __setattr__(self,item,val):
        self[item] = val



class Config(object):

    def __init__(self,filename):
        filename = os.path.expanduser(filename)
        self.data = Level(yaml.safe_load(open(filename,'r')))

    def __getattr__(self,item):
        return self.data[item]

    def __getitem__(self,item):
        return self.data[item]

    def __repr__(self):
        return pprint.pformat(self.data)

#  -------------------------------------------------------------------------
#        Program Logic


cf_file = os.path.expanduser('~/.minus80.conf')

# Check to see if there is a config file available
if not os.path.isfile(cf_file):
    with open(cf_file, 'w') as CF:
        print(default_config, file=CF)

cf = Config(cf_file)
