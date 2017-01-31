'''
Created on 25. 4. 2014

@author: casey
'''
import logging
import os
import json
from enum import Enum
from core.assets.adapters.factory import AdapterFactory

AssetStates = Enum('AssetState','OFFLINE, QUEUED, LOADING, UNLOADING, ONLINE')

class Asset(object):
    '''
    classdocs
    '''



    def __init__(self, config, assetFolder, isLocal=True):
        '''
        Constructor
        '''
        self.asset_folder = assetFolder
        self.config_name = config
        self.id_name = config.split(".")[0]
        self.config = {}
        self.isLocal = isLocal
        self.name = None
	self.version = "N/A"
        self.tools = []
        self.parts = {}
        self.state = AssetStates.OFFLINE
        self.loadConfig()

        

    def loadConfig(self):
            conf = self.__loadKBJson()
            self.config = conf
            self.name = conf["asset"]["name"]
	    self.version = conf["asset"]["version"]
            self.tools = conf["configuration"]["tools"] if isinstance(conf["configuration"]["tools"], list) else [conf["configuration"]["tools"]]
            self.__loadParts(conf["configuration"]["parts"])


    def __getPath(self, path):
        if os.path.isabs(path):
            return path
        else:
            return os.path.normpath(os.path.join(self.asset_folder, path))

    def __loadParts(self, conf):
        for pname, pconfig in conf.iteritems():
            self.parts[pname] = AdapterFactory.make(self.asset_folder, pconfig)


    def __loadKBJson(self):
        '''
        Load config json from KB confign, parse it and return as dict
        @return - loaded config as dict
        '''

        f = open(self.__getPath(self.config_name))
        data = json.loads(f.read())
        f.close()
        return data


    def getPart(self, partName):
        return self.parts[partName]

    def autoload(self, loadQueue):
        if "configuration" in self.config and "auto-load" in self.config["configuration"]:
            if self.config["configuration"]["auto-load"]:
                self.load(loadQueue)

    def drop(self):
        for part in self.parts.values():
            if part.isLoadable() and part.isLoaded():
                self.state = AssetStates.QUEUED
                part.drop()

    def load(self, load_qeue):
        loadable = []
        for part in self.parts.values():
            if part.isLoadable() and not part.isLoaded():
                self.state = AssetStates.QUEUED
                loadable.append(part)
        load_qeue.append([self, loadable])
                
    def isLoaded(self):
        status = True
        for part in self.parts.values():
            if part.isLoadable():
                status = status and part.isLoaded()
        logging.error("status of {0} is {1}".format(self.name, status))
        return status
                
                
    def changeState(self, state):
        self.state = state




