'''
Pakage contains group of class for handling webpage requests. 
'''


from core.web.parser import Parser
import cherrypy

class Root():
    '''
    Root page, handling all request for "/" path.
    '''
    

    def __init__(self):
        '''
        @core - instance of main core class.
        '''
        self.parser = Parser()
        
    @cherrypy.expose        
    def ws(self):
        print "new ws handler!!"
    
    @cherrypy.expose
    def api(self):
        pass

    
    