'''
Created on 13. 4. 2014

@author: casey
'''
import os
import json
import cherrypy
from cherrypy.process import plugins

from core.loader import loadClasses
from core.api._JSONRPC.protocol import AProtocol, ProtocolEndPoint
from core.chain import ChainOfResponsibility

    
class JSONRPCHanlder(plugins.SimplePlugin):
    
    def __init__(self, bus, core):
        plugins.SimplePlugin.__init__(self, bus)
        self.core = core
        self.protocol = None
        self.generateProtocolChain()

    
    def start(self):
        cherrypy.log.error("JSON-RPC Started")

    
    def stop(self):
        cherrypy.log.error("JSON-RPC Stopped")
    
    def callRPC(self, action, version=-1, rpc_args = {}):
        return self.protocol.process(action, version, rpc_args)

    def generateProtocolChain(self):
        classes = loadClasses(os.path.join(os.path.dirname(os.path.abspath(__file__)),'_JSONRPC'), AProtocol, "AProtocol")
        self.protocol = ChainOfResponsibility.generate(classes, ProtocolEndPoint, {'core':self.core})
        
    
    
    
    

