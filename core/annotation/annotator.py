# -*- coding: utf-8 -*-
'''
Created on 17. 4. 2014

@author: casey
'''

class Annotator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

        self.pipeline = None
        self.toolkit = {}


    def createPipeline(self, pipeline):
        self.pipeline = pipeline

    def annotate(self, request):
        self.toolkit[request.tool].process(request)
        #return self.pipeline.process(request)


    def generate_toolkit(self, toolkit, config):
        tools = config["enabled"]
        for ckey, value in config.iteritems():
            if ckey.startswith("tool"):
                key,tool_name,what = ckey.split(".")
                if key == "tool" and tool_name in tools and what =="pipeline":
                    self.toolkit[tool_name] = toolkit.createPipeline(value.split("+"))


    def getTools(self):
        return self.toolkit.keys()

    def getPipeline(self, tool):
        return self.toolkit[tool]

class AnnotationRequest():

    def __init__(self, text = "", tool = "", asset = "", version = -1):
        self.input_data = text
        self.ongoing_data = None
        self.output_data = None
        self.tool = tool
        self.tool_params = {}
        self.assetName = asset
        self.asset = None
        self.version = version
        self.filter = None
        #self.nameRecog = ""


    def parseRPC(self, rpcData):
        self.input_data = rpcData["text"]
        self.tool = rpcData["tool"]
        self.assetName = rpcData["assetName"]
        self.tool_params = rpcData["toolParams"]

    def getResult(self):
        return self.result

    def final_init(self, core):
        self.asset = core.assetManager.getAsset(self.assetName)


    def test_integrity(self):
        pass

    def __tool_available(self):
        pass

    def __asset_available(self):
        pass
