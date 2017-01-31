'''
Created on 24. 4. 2014

@author: casey
'''
import os
import cherrypy

from core.api._JSONRPC.protocol import AProtocol
from core.assets.asset import AssetStates

class Protocol(AProtocol):
    
    
    def __init__(self, core):
        super(Protocol, self).__init__(core)
        self.version = 1

    def RPC_getAssetList(self, toolType):
        assets = self.core.assetManager.getAssets(toolType)
        out = []
        for asset in assets:
            data = {}
            data["status"] = AssetStates.OFFLINE.value-1 if asset.state != AssetStates.ONLINE else AssetStates.ONLINE.value-1
            data["name"] = asset.id_name
            out.append(data)
        return out

    def RPC_getStatus(self, toolType=None):
        assets = self.core.assetManager.getAssets(toolType)
        out = []
        for asset in assets:
            data = self.__get_stats()
            data["status"] = asset.state.value -1 
            data["processor"] = asset.tools if len(asset.tools) > 1 else asset.tools[0]
            data["name"] = asset.id_name
            out.append(data)
        return out
        

    def RPC_loadAsset(self, assetName):
        return self.core.assetManager.loadAsset(assetName)

    def RPC_dropAsset(self, assetName):
        return self.core.assetManager.dropAsset(assetName)

    def RPC_listExampleFiles(self):
        #folder = cherrypy.request.apps[''].config['core']['text_examples']
        folder = self.core.appConfig['core']['text_examples']
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
        cherrypy.response.headers['Content-Type'] = "application/json"
        return files
    
    def RPC_getFileContent(self, filename):
        filename = os.path.basename(filename)
        path = os.path.join(self.core.appConfig['core']['text_examples'],filename)
        with open(path,'r') as f:
            text = f.read()
        return text
    
    def RPC_annotate(self, request):
        request.final_init(self.core)
        self.core.annotator.annotate(request)
        kb = request.asset.getPart("kb")
        groups = {}
        groupsData = {}
        for key, data in kb.groups.iteritems():
            groups[key] = data["name"]
            groupsData[key] = data["dataPlus"]
        return {"header":{"status":0,
                            "msg":"",
                            "processor":request.tool,
                            "groups": groups,
                            "groups_ext": groupsData,
                            "version":self.core.appConfig["versions"]["global"]
                          },
                "result":request.output_data
                }
    
    
    def __get_stats(self):
        return {
                "size":-1,
                "load_time":-1,
                "status":0,
                "processor":None
                }
    