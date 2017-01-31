'''
Created on 10.3.2013

@author: xjerab13
'''

import cherrypy
import json
import os


class Parser():
    '''
    Parser class, handling requests for "/parser"
    '''
    def __init__(self):
        pass
        
    
    @cherrypy.expose    
    def testFilesList(self):
        '''Retrun json of aviable text files for quick testing'''
        #print os.listdir(os.path.join(os.getcwd(),'test'))
        folder = cherrypy.request.app.config['core']['text_examples']
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f))]
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(files)
    
    @cherrypy.expose
    def testFileContent(self, filename):
        '''
        Return content of texting file.
        @filename - name of testing file for load
        @return - content of filename
        '''
        filename = os.path.basename(filename)
        path = os.path.join(cherrypy.request.app.config['core']['text_examples'],filename)
        with open(path,'r') as f:
            text = f.read()
        return text