'''
Created on 11. 5. 2014

@author: casey
'''
from core.pipeline import Pipeline

class AbstractGenerator(Pipeline):
    '''
    classdocs
    '''

    def generate(self, tool_output, asset, version):
        pass