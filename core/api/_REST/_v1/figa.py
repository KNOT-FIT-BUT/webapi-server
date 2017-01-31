# -*- coding: utf-8 -*-
'''
Created on 23. 10. 2013

@author: xjerab13
'''
import cherrypy
from core.annotation.annotator import AnnotationRequest


class FigaHandler():
    '''
    Figa handler server data about aviable FSA automas and parse text via figa tool.
    '''

    exposed = True
    
    def __init__(self):
        '''
        @core - instance of main Core class
        '''
        self.json_rpc = cherrypy.engine.json_rpc
        
    @cherrypy.tools.json_out()
    def GET(self, *flags, **kw):
        '''
        On GET request return json with info about available FSA automats for use.
        @return - JSON to client 
        '''
        return self.json_rpc.callRPC(action = "getAssetList", rpc_args = {"toolType" : "figa"})
        
    
    @cherrypy.tools.json_out()
    def POST(self, *flags, **kw):
        '''
        Performin text parsing via figa tool.
        '''
        txt = kw.get("text")
        asset_name = flags[0] if len(flags) > 0 else None
        return self.json_rpc.callRPC(action = "annotate", rpc_args = {"request" : AnnotationRequest(txt, "figa", asset_name, 1)}, version = 1)
        
    @cherrypy.tools.json_out()
    def PUT(self, kbname):
        '''
        Unused.
        '''
        pass
        
    @cherrypy.tools.json_out()
    def DELETE(self, kbname):
        '''
        Unused
        '''
        pass
    
        