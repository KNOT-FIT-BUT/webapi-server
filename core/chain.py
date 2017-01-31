'''
Created on 1. 5. 2014

@author: casey
'''

class ChainItem(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.nextChainItem = None
        
    def registerNextChainItem(self, item):
        self.nextChainItem = item
    
    def process(self):
        """Wrapper around the internal _hook method"""
        

    def _hook(self):
        """Default hook method to be overridden in subclasses"""

      
class ChainTerminator(ChainItem):
    
    def process(self, **kwargs):
        return self._hook()

    def _hook(self):
        return None
      
      
class ChainOfResponsibility(object):
    
    @classmethod
    def generate(cls, chainList, endClass, chainParams):
        firstItem = endClass()
        for chainItem in chainList:
            newChain = chainItem(**chainParams) if chainParams else chainItem()
            newChain.registerNextChainItem(firstItem)
            firstItem = newChain
        return firstItem