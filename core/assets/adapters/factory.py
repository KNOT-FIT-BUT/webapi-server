'''
Created on 9. 5. 2014

@author: casey
'''
import os
from core.loader import loadClasses
from core.assets.adapters._abstract import AbstractAdapter


class AdapterFactory(object):
    
    adapters = {}
    
    @classmethod
    def make(cls, base_folder, config):
        path = config["target"]
        adapter = config["adapter"]
        adapter_configuration = config["adapter_configuration"]
        if adapter in cls.adapters:
            return cls.adapters[adapter](path, base_folder, adapter_configuration)
        else:
            raise AttributeError("Asset adapter not found: " + adapter)
    
    @classmethod
    def loadAdapters(cls):
        classes = loadClasses(os.path.dirname(os.path.abspath(__file__))+"/_adapters", 
                              AbstractAdapter, ["AbstractAdapter", "AbstractStaticAdapter", "AbstractDynamicAdapter"], False)
        for c in classes:
            cls.adapters[c.__name__] = c