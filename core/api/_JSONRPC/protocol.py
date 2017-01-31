'''
Created on 1. 5. 2014

@author: casey
'''
import inspect

from core.chain import ChainItem, ChainTerminator

class AProtocol(ChainItem):
    '''
    classdocs
    '''


    def __init__(self, core):
        '''
        Constructor
        '''
        super(AProtocol, self).__init__()
        self.core = core
        self.version=0
        self.RPC_methods = []
        self.__loadMethods()
        
        
    def __loadMethods(self):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        self.RPC_methods = [method[0][4:] for method in methods if method[0].startswith("RPC_")]


        
        
    def process(self, action, version, rpc_args):

        if (self.version == version or version == -1) and action in self.RPC_methods:
                return self._hook(action, rpc_args)
        return self.nextChainItem.process(action, version, rpc_args)
    
    def _hook(self, action, rpc_args):
        calle = getattr(self, "RPC_"+action)
        return calle(**rpc_args) if rpc_args else calle()
        
    
class ProtocolEndPoint(ChainTerminator):
    
    def __init__(self):
        super(ProtocolEndPoint, self).__init__()
        self.version = "terminator"


    def process(self, action, version, rpc_args):
        return None
        
    