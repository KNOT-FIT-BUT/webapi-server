'''
Created on 9. 5. 2014

@author: casey
'''
import os, sys


class AbstractAdapter(object):
    '''
    classdocs
    '''


    def __init__(self, target, asset_folder, config):
        '''
        Constructor
        '''
        self.target = target
        self.asset_folder = asset_folder #relative to target path
        self.base_folder = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.config = config
        #self.custom_init()
        
    def preload_init(self):
        #only for local path - remote target will be memory name = exception
        abs_path = self.getNormalizedPath(self.asset_folder, self.target) 
        if not os.path.exists(abs_path):
            raise Exception(("Asset part not found no selected path {0}").format(abs_path))
        
        
    def getNormalizedPath(self, base, path):
        if os.path.isabs(path):
            return path
        else:
            return os.path.normpath(os.path.join(base, path))
        
    def getTargetPath(self):
        return self.getNormalizedPath(self.asset_folder, self.target)
    


class AbstractDynamicAdapter(AbstractAdapter):
    

    def load(self):
        pass
    
    
    def drop(self):
        pass

    def postload_init(self):
        pass

    def isLoaded(self):
        return False
    
    def isLoadable(self):
        return True


class AbstractStaticAdapter(AbstractAdapter):
    

    def isLoadable(self):
        return False