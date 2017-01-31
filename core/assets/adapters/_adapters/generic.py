'''
Created on 9. 5. 2014

@author: casey
'''
from core.assets.adapters._abstract import AbstractStaticAdapter


class GenericAsset(AbstractStaticAdapter):
        
    def __init__(self, target, base_folder, config):
        super(GenericAsset, self).__init__(target, base_folder, config)
        
    