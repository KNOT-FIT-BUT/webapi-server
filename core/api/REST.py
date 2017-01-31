'''
Created on 13. 4. 2014

@author: casey
'''
import cherrypy

from _REST.restV1 import RESTService


class RESTHandler():
    
    def __init__(self):
        self.v1 = RESTService()
    

    def GET(self):
        raise cherrypy.HTTPError(404)
    
    def POST(self):
        raise cherrypy.HTTPError(404)
    
    def PUT(self):
        raise cherrypy.HTTPError(404)
    
    def DELETE(self):
        raise cherrypy.HTTPError(404)