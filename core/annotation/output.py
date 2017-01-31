'''
Created on 17. 4. 2014

@author: casey
'''
import os
from core.pipeline import Pipeline
from core.loader import loadClasses
from core.annotation.generators._abstract import AbstractGenerator

class ResultGenerator(Pipeline):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Pipeline.__init__(self)
        self.generators = {}
        self.loadGenerators()
        
        
    def _hook(self, request):
        self.generateOutput(request)
        
        
    def generateOutput(self, request):
        request.result = self.generators[request.tool].generate(request.ongoing_data, request.asset, request.version)
        del(request.ongoing_data)
    
    
    def loadGenerators(self):
        classes = loadClasses(os.path.dirname(os.path.abspath(__file__))+"/generators/", AbstractGenerator, "AbstractGenerator")
        for c in classes:
            self.generators[c.forTool] = c()
    
    
        
