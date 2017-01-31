# -*- coding: utf-8 -*-
'''
Created on 24. 4. 2014

@author: casey
'''
import os
from core.api._JSONRPC.protocol import AProtocol
from core.annotation.generators.genkit.v2 import generateKBRecords, generateGroups
from core.annotation.filters.inputFilters import UTFEncode
from collections import OrderedDict
#from nameRecog import process_outputs as po
from name_recognizer import process_outputs as po

toolsParams = {"ner":["lower","remove accent","name_recognize"],
               "figa":["overlapping","boundary"]
                  }

class Protocol(AProtocol):



    def __init__(self, core):
        super(Protocol, self).__init__(core)
        self.version = 2


    def RPC_getWebapiInitPack(self):
        assets = self.core.assetManager.getAssets()
        assets_data = {}

        tools = {}
        for tool in self.core.annotator.getTools():
            tools[tool] = { "name":tool,
                            "params":toolsParams[tool] if tool in toolsParams else [],
                            "version" : " 2f034e96d0e31deb01b49725f5878c6d0a629bd2"

            }

        for asset in assets:
            assets_data[asset.id_name] = {
                     "name":asset.name,
                     "description":"",
		     "version":asset.version,
                     "type":"",
                     #"tools":asset.tools if len(asset.tools) > 1 else asset.tools[0],
                     "tools":asset.tools,
                     "state":asset.state.value -1
                    }
        pack = {
                #"tools":self.core.annotator.getTools(),
                "tools":tools,
                "assets":assets_data,
                "example_files":self.nextChainItem.process("listExampleFiles", 1, {}),
                "configs":[]
                }
        return pack


    def RPC_getFile(self, filename):
        return self.nextChainItem.process("getFileContent", 1, {"filename":filename})

    def RPC_getConfig(self, filename):
        pass

    def RPC_loadAsset(self, assetName):
        print "Request to load asset", assetName
        self.core.assetManager.loadAsset(assetName)

    def RPC_dropAsset(self, assetName):
        print "Request to drop asset", assetName
        self.core.assetManager.dropAsset(assetName)

    def RPC_annotate(self, request):
        request.final_init(self.core)
        #if "name_recognize" in request.tool_params and request.tool_params["name_recognize"] and False:
        #    folder = self.core.appConfig['namerecog']["n.folder"]
        #   asset = self.core.appConfig['namerecog']["n.asset"]
        #    utffilter  = UTFEncode()
        #    request.nameRecog = self.core.toolkit.getTool('Figa')().call_raw(utffilter.encode(request.input_data), os.path.join(folder,asset))
        self.core.annotator.annotate(request)
        request.output_data["header"] = {}
        return request.output_data

    def RPC_autocomplete(self, inputData, automat):
        kb = self.core.assetManager.getAsset("KBstatsMetrics").getPart("kb")
        if not kb.isLoaded():
            return {}
        folder = self.core.appConfig['autocomplete']["ac.folder"]
        utffilter  = UTFEncode()
        partialResult = self.core.toolkit.getTool('Figa')().autocomplete(utffilter.encode(inputData), os.path.join(folder,automat), 5)

        kb_records = generateKBRecords(partialResult, kb)
        partialMatch = []
        others = []
        inputTextRaw = inputData.lower().strip()
#         for entity in partialResult:
#             kb_records.add(entity.preferred_sense)
#             kb_records.update(entity.senses)
#             item={"name":entity.source,
#                   "preffered":entity.preferred_sense,
#                   "others": entity.senses[1:] if entity.preferred_sense in entity.senses else entity.senses
#                   }
#             entities[cnt] = item
#             cnt+=1
        for key,data in kb_records.items():

            Ename = [data.get(column) for column in ['name','display term'] if data.get(column, None) is not None][0].lower()
            #print Ename,inputTextRaw,inputTextRaw in Ename
            if inputTextRaw in Ename:
                partialMatch.append((key,data))
            else:
                others.append((key,data))

        partialMatch = sorted(partialMatch, key=lambda x: x[1]["confidence"], reverse=True)
        others = sorted(others, key=lambda x: x[1]["confidence"], reverse=True)
        final = partialMatch + others
        finalslice = {a:b for a,b in final[:10]}
        return {
                "kb_records":finalslice,
                "entities":None,
                "items":None,
                "groups":generateGroups(kb)
                }

    def RPC_getAutocompleteInitPack(self):
        folder = self.core.appConfig['autocomplete']["ac.folder"]
        extension = self.core.appConfig['autocomplete']["ac.extension"].encode("utf-8")
        ignore = self.core.appConfig['autocomplete']["ac.ignore"]
        print extension
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) and os.path.splitext(f)[1]==extension and f not in ignore]
        print [os.path.isfile(os.path.join(folder,f)) for f in os.listdir(folder) ]
        return {"automats":files}


    def RPC_nameRecognition(self, inputData):
        result = []
        folder = self.core.appConfig['namerecog']["n.folder"]
        asset = self.core.appConfig['namerecog']["n.asset"]
        utffilter  = UTFEncode()
        partialResult = self.core.toolkit.getTool('Figa')().call_raw(utffilter.encode(inputData), os.path.join(folder,asset))
        figaready = []
        for line in partialResult.split("\n"):
            x = "\t".join(line.split("\t")[:4])
            figaready.append(x)
        figaready = ("\n").join(sorted(figaready))
        if len(figaready) > 0:
            d = po.Document(figaready, inputData, False, po.OUT_FILTERED, po.OUT_LEARNED , po.TOLERANCE, False)
            d.analyze()
            if d.name_list != []:
                tlist = sorted(d.name_list)
                for d in tlist:
                    result.append([d.type, d.start_offset, d.end_offset, d.value])
        return result
