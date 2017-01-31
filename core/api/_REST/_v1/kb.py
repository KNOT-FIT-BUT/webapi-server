'''
Created on 28. 10. 2013

@author: xjerab13
'''
import cherrypy
from core.annotation.annotator import AnnotationRequest

class KBHandler():
    '''
    KBHandler controling and server info about available Knowledge Bases
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
        Return info about KB. Info type is determined by flags variable
        @flags - contains url parameters 
        @return - data JSON with info about KB 
        '''
        if "reload" in flags:
            pass
            #reload from folder
        elif "loaded" in flags:
            pass
            #return list of loaded KBs
        else:
            try:
                data = self.json_rpc.callRPC(action = "getStatus")
                return data
            except AttributeError, e:
                print "attr error ", e
                raise cherrypy.HTTPError(404) 
            
    
    @cherrypy.tools.json_out()
    def POST(self, *flags, **kw):
        pass
        
    @cherrypy.tools.json_out()
    def PUT(self, kbname):
        '''
        Add KB to load queue.
        @kbname - KB filename without extension
        '''
        #self.asset_manger.loadKB(kbname)
        self.json_rpc.callRPC("loadAsset", rpc_args = {"assetName":kbname})
        pass
        
    @cherrypy.tools.json_out()
    def DELETE(self, kbname):
        '''
        Add KB to unload queue.
        @kbname - KB filename without extension.
        '''
        #self.asset_manger.dropKB(kbname)
        self.json_rpc.callRPC("dropAsset", rpc_args = {"assetName":kbname})
        pass
    
    