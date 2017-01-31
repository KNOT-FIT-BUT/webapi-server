'''
Created on 16. 4. 2014

@author: casey
'''
import cherrypy


from annotation.annotator import Annotator
from assets.manager import AssetManager
from annotation.toolkit import Toolkit
from assets.adapters.factory import AdapterFactory

class AppCore(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.annotator = None
        self.assetManager = None
        self.appConfig = None
        
    def inito(self):
        app = cherrypy.tree.apps['']
        self.appConfig = app.config
        AdapterFactory.loadAdapters()
        self.toolkit = Toolkit(app.config["pipelines"])
        #self.resultFactory = ResultGenerator()
        self.assetManager = AssetManager()
        self.assetManager.start()
        self.assetManager.loadAssetsForTools(self.toolkit.getTools())
        self.assetManager.autoload()
        
        self.annotator = Annotator()
        self.annotator.generate_toolkit(self.toolkit, app.config["annotator"],)
        #self.annotator.createPipeline(self.toolkit + self.resultFactory)   
   
        
    def destroy(self):
        cherrypy.log.error("CORE Stopped")
        self.assetManager.stop()
        
        