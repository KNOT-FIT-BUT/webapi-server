'''
Created on 17. 4. 2014

@author: casey
'''
import os

from core.pipeline import Pipeline
from core.loader import loadClasses
from tools._abstract import AbstractTool
from filters._abstract import AbstractFilter
from generators._abstract import AbstractGenerator


class Toolkit():
    
    conf =    {
     "tools":[os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'), AbstractTool, "AbstractTool"],
     "filters":[os.path.join(os.path.dirname(os.path.abspath(__file__)),'filters'), AbstractFilter, "AbstractFilter"],
     "generators":[os.path.join(os.path.dirname(os.path.abspath(__file__)),'generators'), AbstractGenerator, "Generator"]
    }
    
    blocks = {
      "f":"filters",
      "t":"tools",
      "g":"generators",
      "p":"shared_pipelines"
              }
    
    def __init__(self, pipelines):
        self.filters = {}
        self.generators = {}
        self.tools = {}
        self.namedTools = {}
        self.initialize()
        self.shared_pipelines = {}
        self.pregenerate_pipelines(pipelines)

        
    def initialize(self):
        for key, conf in Toolkit.conf.iteritems():
            classes = loadClasses(*conf)
            block = getattr(self, key)
            for c in classes:
                block[c.__name__]=c
                print c
        
    def pregenerate_pipelines(self, pipelines):
        for key, value in pipelines.iteritems():
            self.shared_pipelines[key] = [self.getBlock(*block.split(".")) for block in value.split("+")]

        
    def getBlock(self, block, name):
        group = getattr(self, Toolkit.blocks[block])
        if name in group:
            return group[name]
        else:
            pass
    
    def getBlockInstance(self, block, name):
        sup = self.getBlock(block, name)
        if isinstance(sup, list):
            ret = sup[0]()
            for r in sup[1:]:
                ret + r()
            return ret 
        else:
            return sup()
    
    def createPipeline(self, pipeline):
        result = None
        for block in pipeline:
            if result is None:
                result = self.getBlockInstance(*block.split("."))
            else:
                result + self.getBlockInstance(*block.split("."))
        return result
        
    
    def getTools(self):
        return self.tools
    
    def getTool(self, tool):
        print tool, self.tools
        return self.tools[tool] if tool in self.tools else None

class Toolkito(Pipeline):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Pipeline.__init__(self)
        self.tools = {}
        self.loadTools(Tool)
        
    def _hook(self, request):
        tool, args = self.prepareToolArgumens(request)
        request.ongoing_data = self.callTool(tool, args)
        
    def callTool(self, tool, args):
        return self.tools[tool].call(**args)
        
    def prepareToolArgumens(self, request):
        tool = self.tools[request.tool]
        args = {}
        for r in tool.require:
            args[r] = getattr(request,r)
        return request.tool, args
    
    def loadTools(self, base_class):
        classes = loadClasses(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tools'), base_class, "Tool")
        for c in classes:
            self.tools[c.toolName]=c()
        
    def getTools(self):
        return self.tools
            
        