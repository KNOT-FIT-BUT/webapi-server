'''
Created on 17. 4. 2014

@author: casey
'''

import os
import cherrypy
import time
import sys

from threading import Thread, Event
from collections import deque


from core.assets.asset import Asset, AssetStates
import traceback


class AssetManager(Thread):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Thread.__init__(self)
        app = cherrypy.tree.apps['']

        self.base_folder = app.config["global"]["tools.staticdir.root"]
        asset_folder = app.config["assets"]["asset.folder"]
        self.asset_folder = asset_folder if os.path.isabs(asset_folder) else os.path.join(self.base_folder, asset_folder)
        self.asset_extension = app.config["assets"]["asset.extension"]

        self.assets = {}  # new !
        self.assets_online = []
        
        self.do = Event()
        self.quit = Event()

        self.load_qeue = deque()

    def loadLocalAssets(self, folder):
        assets = []
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        for filename in set(files):
            if os.path.splitext(filename)[1] == self.asset_extension:
                try:
                    asset = Asset(filename, self.asset_folder)
                    # assets[asset.name] = asset
                    assets.append(asset)
                except IOError, e:
                    print "IOerror", e
                except TypeError, e:
                    print "Type error", e
                except Exception, e:
                    traceback.print_tb(sys.exc_info()[2])
                    print "general error", e
                finally:
                    pass
        return assets
    
    def loadSharedAssets(self):
        pass

    def loadAssetsForTools(self, tools):
        assets = self.loadLocalAssets(self.asset_folder)
        toolList = tools.keys()
        for asset in assets:
            isCompatible = [tools[tool].testAssetCompatibility(asset) for tool in toolList]
            if not False in isCompatible:
                #self.assets[asset.name] = asset
                self.assets[asset.id_name] = asset

    def run(self):
        self.quit.clear()
        self.do.clear()
        while not self.quit.isSet():
            if self.do.isSet():
                while len(self.load_qeue) > 0:
                    asset, loadable = self.load_qeue.pop()
                    print asset.id_name
                    asset.changeState(AssetStates.LOADING)
                    for part in loadable:
                        part.load()
                    if asset.isLoaded():
                        asset.changeState(AssetStates.ONLINE)
                self.do.clear()
            time.sleep(0.1)

    def stop(self):
        
        for asset in self.assets.values():
            asset.drop()
        
        self.quit.set()
        self.join()

    def getAssets(self, tool = None, in_state=None):
        subset = self.assets.values()
        if tool is not None:
            subset = [asset for asset in subset if tool in asset.tools]
        if in_state in AssetStates:
            subset = [asset for asset in subset if asset.state == in_state] 
        return subset

 
    def getAsset(self, a_name):
        '''
        @a_name - name of asset 
        @return asset instance container or None
        '''
        return self.assets[a_name]
    
    def getLoaded(self):
        '''
        @return - list of names of loaded KB
        '''
        return [k for k in self.loaded if self.kb_list[k].status == 4]

    def loadAsset(self, asset_name):
        if asset_name in self.assets.keys():
            self.assets[asset_name].load(self.load_qeue)
            self.do.set()

    def dropAsset(self, asset_name):
        pass

    def autoload(self):
        '''
        Add all KB marked for autoload to load queue.
        '''
        for asset in self.assets.values():
            asset.autoload(self.load_qeue)
        self.do.set()

    def loadColumsFromFile(self, filename):
        column_ext_def = {"g": {"type": "image"},
                          "u": {"type": "url"}
                          }

        columns = {}
        columns_ext = {}
        prefix_desc = {}
        with open(filename, 'r') as f:
            raw_colums = f.read().strip()

        for row in raw_colums.split("\n"):
            column = []
            row_split = row.split("\t")
            row_head = row_split.pop(0)
            row_prefix, row_head, row_id = row_head.split(":")
            prefix_desc[row_prefix] = row_head.lower()
            column.append(row_id.lower())
            for col_name in row_split:
                prefix = ""
                url = ""
                if ':' in col_name:
                    col_split = col_name.split(":")
                    prefix = ":".join(col_split[:-1])
                    if "[" in prefix:
                        prefix, url = prefix.split("[")
                    col_name = col_split[-1]
                    for k in prefix:
                        if k in column_ext_def:
                            if row_prefix not in columns_ext:
                                columns_ext[row_prefix] = {}
                            columns_ext[row_prefix][col_name.lower()] = {
                                "type": column_ext_def[k]["type"],
                                "data": url[:-1]
                            }
                    if "m" in prefix:
                        col_name = "*" + col_name
                column.append(col_name.lower())
            columns[row_prefix] = column
        columns["prefix_desc"] = prefix_desc
        columns["columns_ext"] = columns_ext
        return columns
