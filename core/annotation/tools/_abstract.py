'''
Created on 24. 4. 2014

@author: casey
'''
from core.pipeline import Pipeline

class AbstractTool(Pipeline):
    '''
    classdocs
    '''
    
    
    def __init__(self, config = None):
        '''
        Constructor
        '''
        super(AbstractTool, self).__init__()
        self.config = config
    
    def call(self, tool, input_data, params):
        raise Exception("Do not call, abstract class!")
    
    @classmethod
    def testAssetCompatibility(self, asset):
        return True