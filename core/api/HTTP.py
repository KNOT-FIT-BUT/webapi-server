'''
Created on 13. 4. 2014

@author: casey
'''
import cherrypy
import json
from core.annotation.annotator import AnnotationRequest

class HTTPHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.json_rpc = cherrypy.engine.json_rpc
        
        
    @cherrypy.expose
    def default(self):
        return "QQ"
    
    @cherrypy.expose
    @cherrypy.tools.json_out()    
    def files(self, func=None):
        return self.json_rpc.callRPC(action = "getAutocompleteInitPack", version = 2, rpc_args = None)
        
    @cherrypy.expose
    @cherrypy.tools.json_out() 
    def jsonrpc(self):
        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)
        if body["method"] == "annotate":
            request = AnnotationRequest(version=2)
            request.parseRPC(body["params"])
            result = self.json_rpc.callRPC(action = "annotate", version = 2, rpc_args = {"request":request})
        else:
            result = self.json_rpc.callRPC(action = body["method"], version = -1, rpc_args = body["params"])
        resp = {"jsonrpc": "2.0", "result": result, "id": body["id"], "source":body["method"], "mods":{}}
        if "offset" in body.get("mods",{}):
            resp["mods"]["offset"]=body["mods"]["offset"]
        return resp
    
    