'''
Pakage contains group of class for handling REST API requests. 
'''
import cherrypy


from core.api._REST._v1 import FigaHandler, NERHandler, KBHandler


class RESTService():
    '''
    Core class for handling http request and building substructure of REST API.
    '''
    exposed = True
    
    def __init__(self):
        '''
        Inintialize class. 
        @core - insgtance of main Core class
        '''
        #self.base_folder = core.base_folder
        #self.kbmanager = core.getManager("kb")
        self.kb = KBHandler()
        self.figa = FigaHandler()
        self.ner = NERHandler()
        

    @cherrypy.tools.json_out()
    def GET(self, *flags, **kw):
        raise cherrypy.HTTPError(404)
    
    @cherrypy.tools.json_out()
    def POST(self, *flags, **kw):
        raise cherrypy.HTTPError(404)
        
    
    def PUT(self):
        raise cherrypy.HTTPError(404)
        
    
    def DELETE(self):
        raise cherrypy.HTTPError(404)
    
    

        
        
    
    
    
    
