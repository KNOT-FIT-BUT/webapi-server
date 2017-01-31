# -*- coding: utf-8 -*-
'''
Created on 9. 5. 2014

@author: casey
'''
import os, re
import gc
import commands
from ctypes import cdll, POINTER, c_char_p, c_int, c_void_p

from core.assets.adapters._abstract import AbstractDynamicAdapter
from core.assets.adapters._adapters.functions import loadHeaderFromFile




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
    
    


    