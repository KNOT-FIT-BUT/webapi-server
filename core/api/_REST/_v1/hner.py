# -*- coding: utf-8 -*-
'''
Created on 28. 10. 2013

@author: xjerab13
'''

import cherrypy

from core.annotation.annotator import AnnotationRequest



class NERHandler():
    '''
    NERHandler serve data about available KB for NER and parsing text via NER tool.
    '''

    exposed = True
    def __init__(self):
        '''
        @ore - instance of main Core class.
        '''
        self.json_rpc = cherrypy.engine.json_rpc
        
    @cherrypy.tools.json_out()
    def GET(self, *flags, **kw):
        '''
        On GET return info about all available KB.
        '''
        
        return self.json_rpc.callRPC(action = "getAssetList", rpc_args = {"toolType": "ner"})
    
    
    @cherrypy.tools.json_out()
    def POST(self, *flags, **kw):
        '''
        Paring text via NER tool.
        @return - data JSON to client.
         '''
        txt = kw.get("text")
        asset_name = flags[0] if len(flags) > 0 else None
        return self.json_rpc.callRPC(action = "annotate", rpc_args = {"request" : AnnotationRequest(txt, "ner", asset_name, 1)}, version = 1)
            
    
    def PUT(self):
        pass
        
    
    def DELETE(self):
        pass

        
        