# -*- coding: utf-8 -*-
'''
Created on 9. 5. 2014

@author: casey
'''
import os, re
import gc
import commands
from ctypes import cdll, POINTER, c_char_p, c_int, c_void_p

from knowledge_base import KnowledgeBase
from core.assets.adapters._abstract import AbstractDynamicAdapter
from core.assets.adapters._adapters.functions import loadHeaderFromFile


class KBner(AbstractDynamicAdapter):
    '''
    Adapter for Knowledge_Base class from NER library. This class encapsulate behavior for webapi loading
    and unloading KB, all other calls are passed to original NER class.
    '''
    
    def __init__(self, target, base_folder, config):
        super(KBner, self).__init__(target, base_folder, config)
        self._kb = None
        self.groups = {}
        self.groupsData = {}
        self.preload_init()
        
        
    def preload_init(self):
        AbstractDynamicAdapter.preload_init(self)
        config_header = self.config["header"] 
        if config_header["external_file"]:
            self.header, self.groups = loadHeaderFromFile(self.getNormalizedPath(self.asset_folder, config_header["external_file"]))
        elif config_header["custom"]:
            self.header = {"generic":config_header["custom"]["generic"]}
            self.groups = {"generic":config_header["custom"]["data"]}
        
        if "value_splitter" in self.config:
            self.value_splitter = self.config["value_splitter"].encode("utf-8") if self.config["value_splitter"] is not None else "".encode("utf-8")
        
    def load(self):
        '''
        Load KB into memory.
        '''
        self._kb = KnowledgeBase(self.getNormalizedPath(self.asset_folder, self.target))
        
    def drop(self):
        '''
        Dealocate KB from memory.
        '''
        maxitem = 33 
        lib = cdll.LoadLibrary(os.path.join(self.base_folder, "api","NER","figa","sources","kb_loader.so"))
        lib.queryTree.restype = c_void_p
        lib.queryTree.argtypes = [POINTER(POINTER(c_char_p)),c_int,c_int]

        lib.freeTree(self._kb.lines, self.kb_path,self._kb.items_number, maxitem);
        del(self._kb.lines)
        self._kb.lines = None
        self.status = 0
        gc.collect()
        
    
    
    def __getattr__(self, attr):
        '''
        Pass all method calls or variable requests to instance of NER KnowledgeBase class.
        '''
        attribute = getattr(self._kb, attr)
        if callable(attribute): 
            def wrapper(*args, **kw):
                return attribute(*args, **kw)
            return wrapper
        else:
            return attribute

    def isLoaded(self):
        return True if (self._kb is not None and self._kb.lines is not None) else False



                


class KBgeneric(AbstractDynamicAdapter):
    
    def __init__(self, target, base_folder, config):
        super(KBgeneric, self).__init__(target, base_folder, config)
        self.lines = None
        self.items_number = None
        self.header = {}
        self.groups = {}
        self.groupsData = {}
        self.preload_init()
        
    def preload_init(self):
        AbstractDynamicAdapter.preload_init(self)
        config_header = self.config["header"] 
        if config_header["external_file"]:
            self.header, self.groups = loadHeaderFromFile(self.getNormalizedPath(self.asset_folder, config_header["external_file"]))
        elif config_header["custom"]:
            self.header = {"generic":config_header["custom"]["generic"]}
            self.groups = {"generic":config_header["custom"]["data"]}
        
    def load(self):
        
        '''
        Load KB from file via kb_loader.so.
        '''
        target_path = self.getNormalizedPath(self.asset_folder, self.target)
        count = commands.getoutput('wc -l ' + target_path + ' | cut -d" " -f1')
        self.items_number = int(count)
        maxitem = 33 
        lib = cdll.LoadLibrary( os.path.join(self.base_folder, "api","NER","figa","sources","kb_loader.so"))
        lib.queryTree.restype = POINTER(POINTER(c_char_p))
        lib.queryTree.argtypes = [c_char_p,c_int,c_int]

        self.lines = lib.queryTree(target_path, self.items_number, maxitem);
        
    def _drop(self):
        '''
        Dealoc KB from memory via kb_loader.so
        '''
        target_path = self.getNormalizedPath(self.asset_folder, self.target)
        maxitem = 33 
        lib = cdll.LoadLibrary(os.path.join(self.base_folder, "api","NER","figa","sources","kb_loader.so"))
        lib.queryTree.restype = c_void_p
        lib.queryTree.argtypes = [POINTER(POINTER(c_char_p)),c_int,c_int]
        lib.freeTree(self.lines, target_path, self.items_number, maxitem);
        del(self.lines)
        self.lines = None
        gc.collect()
        
        
    def get_field(self, line, column):
        """Returns a column of a line in the knowledge base"""
        #KB lines are indexed from one
        return self.lines[int(line) - 1][column] if (self.items_number >= int(line)) else None
    
    
    def get_row(self, line):
        '''
        @return - list of KB row data
        '''
        return self.lines[int(line) -1]
    
    def isLoaded(self):
        '''
        Return True if KB is loaded into memory or False.
        '''
        return True if self.lines else False
    
    


    