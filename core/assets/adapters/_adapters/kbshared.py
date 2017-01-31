# -*- coding: utf-8 -*-
'''
Created on 13. 5. 2014

@author: casey
'''

import os, re
import gc
import commands
from ctypes import cdll, POINTER, c_char_p, c_int, c_void_p

from core.assets.adapters._abstract import AbstractDynamicAdapter

from collections import OrderedDict
import logging
from core.assets.adapters._adapters.functions import loadHeaderFromFile
import ner_knowledge_base 

class KBnerFakeShared(AbstractDynamicAdapter):
    
    
    def __init__(self, target, base_folder, config):
        super(KBnerFakeShared, self).__init__(target, base_folder, config)
        self.header = OrderedDict()
        self.groups = {}
        self.clean_header = OrderedDict()
        self.value_splitter = ""
        self.lines = None
        self.name_dict = {}
        self.items_number = 0
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

        for prefix, columns in self.header.iteritems():
            self.clean_header[prefix] = [col.upper() if not col.startswith("*") else col[1:].upper() for col in columns] 
        
    def load(self):
        
        '''
        Load KB from file via kb_loader.so.
        '''
        logging.error("LOADING+++++++++ " + self.value_splitter)
        target_path = self.getNormalizedPath(self.asset_folder, self.target)
        count = commands.getoutput('wc -l ' + target_path + ' | cut -d" " -f1')
        self.items_number = int(count)
        maxitem = 33 
        lib = cdll.LoadLibrary( os.path.join(self.base_folder, "api","NER","figav08","figa","kb_loader.so"))
        lib.queryTree.restype = POINTER(POINTER(c_char_p))
        lib.queryTree.argtypes = [c_char_p,c_int,c_int]
        logging.error("+++++++++++loading")
        self.lines = lib.queryTree(target_path, self.items_number, maxitem);
        self.initName_dict()
    
    def drop(self):
        '''
        Dealocate KB from memory.
        '''
        target_path = self.getNormalizedPath(self.asset_folder, self.target)
        maxitem = 33 
        lib = cdll.LoadLibrary(os.path.join(self.base_folder, "api","NER","figav08","figa","kb_loader.so"))
        lib.queryTree.restype = c_void_p
        lib.queryTree.argtypes = [POINTER(POINTER(c_char_p)),c_int,c_int]

        lib.freeTree(self._kb.lines, target_path, self._kb.items_number, maxitem);
        del(self.lines)
        self.lines = None
        gc.collect()
        
    def isLoaded(self):
        '''
        Return True if KB is loaded into memory or False.
        '''
        return True if (self.lines is not None) else False


    def initName_dict(self):
        '''
        Dictionary asociates people names with items of knowledge base.
        '''
        p_alias = self.get_head_col('p', "ALIAS")
        p_name = self.get_head_col('p', "NAME")
        a_other = self.get_head_col('a', "OTHER TERM")
        a_preferred = self.get_head_col('a', "PREFERRED TERM")
        a_display = self.get_head_col('a', "DISPLAY TERM")
        
        regex_place = re.compile(" of .*")
        
        self.name_dict = {}
        line = 1
        str = self.get_data_at(line, 1)
        while str != None:
            ent_prefix = self.get_ent_prefix(line)
            # PERSON nebo ARTIST
            if ent_prefix == 'p' or ent_prefix == 'a':
                # PERSON
                if ent_prefix == 'p':
                    
                    whole_names = self.get_data_at(line, p_alias).split(self.value_splitter)
                    whole_names.append( self.get_data_at(line, p_name) )
                # ARTIST
                elif ent_prefix == 'a':
                    whole_names = self.get_data_at(line, a_other).split(self.value_splitter)
                    whole_names.append( self.get_data_at(line, a_preferred) )
                    whole_names.append( self.get_data_at(line, a_display) )
                
                names = set()
                for whole_name in whole_names:
                    whole_name = regex_place.sub("", whole_name)
                    divided = whole_name.split(' ')
                    names |= set(divided)
                
                for name in names:
                    if name not in self.name_dict:
                        self.name_dict[name] = set([line])
                    else:
                        self.name_dict[name].add(line)
            line += 1
            str = self.get_data_at(line, 1)

    def get_field(self, line, column):
        '''
        original method 
        '''
        return self.lines[int(line) - 1][column] if (self.items_number >= int(line)) else None
    
    def get_data_at(self, line, col):
        '''
        cislování řádků i sloupců od 1.
        '''
        return self.get_field(line, col-1)
    
    def get_data_for(self, line, col_name):
        '''
        1) zjistit pozici sloupce
        2) dle pozcie zavolat get_field()
        '''
        prefix = self.get_field(line, 0).split(":")[0]
        header_line = self.clean_header[prefix]
        col_position = header_line.index(col_name)
        return self.get_field(line, col_position)
    
    def get_head_at(self, line, col):
        '''
        Číslování řádků i sloupců od 1.
        '''
        key = self.clean_header.keys()[line-1]
        return self.clean_header[key][col-1]
        
    
    def get_head_for(self, prefix, col):
        '''
        Číslování sloupců od 1.
        '''
        return self.clean_header[prefix][col-1]
    
    def get_head_col(self, prefix, col_name):
        '''
        Vrátí číslo sloupce pro požadovaný prefix a jméno sloupce.
        '''
        
        line = self.clean_header[prefix]
        return line.index(col_name)+1
    
    def get_complete_data(self, line, delim='\t'):
        '''
        Vrátí tuple(počet sloupců, celý řádek), kde v jednom řetězci je celý řádek pro požadovaný line, tak jak je v "KB.all".
        Parametr delim umožňuje změnit oddělovač sloupců.
        '''
        text_line = ""  
        col = 1
        str = self.get_data_at(line, col)
        
        if str != None:
                text_line += str
                col += 1  
                str = self.get_data_at(line, col)
        
        while str != None:
                text_line += delim
                text_line += str
                col += 1
                str = self.get_data_at(line, col)
        
        return (col-1, text_line)
    
    def get_complete_head(self, prefix, delim='\t'):
        '''
        Vrátí tuple(počet sloupců, celý řádek), kde v jednom řetězci je celý řádek pro požadovaný line, tak jak je v "KB.all".
        Parametr delim umožňuje změnit oddělovač sloupců.
        '''
        text_line = ""  
        col = 1
        str = self.get_head_for(prefix, col)
        
        if str != None:
                text_line += str
                col += 1  
                str = self.get_head_for(prefix, col)
        while str != None:
                text_line += delim
                text_line += str
                col += 1
                str = self.get_head_for(prefix, col)

        return (col-1, text_line)
    
    def get_ent_prefix(self, line):
        return self.get_field(line, 0).split(":")[0]
    
    def get_ent_type(self, line):
        """Returns a type of an entity at the line of the knowledge base"""
        return self.get_data_for(line, "TYPE")
    
    def get_dates(self, line):
        ent_prefix = self.get_ent_prefix(line)
        if ent_prefix == 'p' or ent_prefix == 'a': # PERSON nebo ARTIST
            dates = set([self.get_data_for(line, "DATE OF BIRTH"), self.get_data_for(line, "DATE OF DEATH")])
        return dates
    
    def get_location_code(self, line):
        return self.get_data_for(line, "FEATURE CODE")[0:3]
    
    def get_nationalities(self, line):
        ent_prefix = self.get_ent_prefix(line)
        if ent_prefix == 'n': # NATIONALITY
            nation = self.get_data_for(line, "ALIAS").split(self.value_splitter)
            nation.extend(self.get_data_for(line, "ADJECTIVAL FORM").split(self.value_splitter))
            nation.append(self.get_data_for(line, "NAME"))
            nation.append(self.get_data_for(line, "COUNTRY NAME"))
        elif ent_prefix == 'p': # PERSON
            nation = self.get_data_for(line, "NATIONALITY").split(self.value_splitter)
        elif ent_prefix == 'a': # ARTIST
            nation = self.get_data_for(line, "OTHER NATIONALITY").split(self.value_splitter)
            nation.append(self.get_data_for(line, "PREFERRED NATIONALITY"))
        new_nation = []
        for nat in nation:
            new_nation.append(nat.lower())
        nation = new_nation
        nation = set(nation)
        return nation
    
    def get_score(self, line, wiki):
        """
        If wiki is true, returns disambiguation score based on Wikipedia
        statistics, if not score based on other metrics.
        """
        result = ""
        if wiki:
            result = self.get_data_for(line, "SCORE WIKI")
        else:
            result = self.get_data_for(line, "SCORE METRICS")
        
        try:
            return int(result)
        except:
            err_prefix = self.get_ent_prefix(line)
            if err_prefix == None:
                err_head = (None, None)
                err_data = (None, None)
            else:
                err_head = self.get_complete_head(err_prefix)
                err_data = self.get_complete_data(line)
            raise
    
    def get_wiki_value(self, line, column_name):
        """
        Return a link to Wikipedia or a statistc value identified
        by column_name from knowledge base line.
        """
        column_rename = {'backlinks':"WIKI BACKLINKS", 'hits':"WIKI HITS", 'ps':"WIKI PRIMARY SENSE"}
        if column_name == 'link':
            return self.get_data_for(line, "WIKIPEDIA URL")
        else:
            return self.get_data_for(line, column_rename[column_name])
    
    def people_named(self, name):
        split_name = name.split(' ')
        result = self.name_dict.get(split_name[0], set())
        for name_part in split_name:
            if name_part in self.name_dict:
                result &= self.name_dict[name_part]
        return result
    
class KBnerShared(AbstractDynamicAdapter):
    #kbd_dir, kbd_path, kb_path,
    def __init__(self, target, base_folder, config):
        super(KBnerShared, self).__init__(target, base_folder, config)
        ner_knowledge_base.update_globals(os.path.join(self.base_folder,"api","SharedKB","var2"),self.getTargetPath())
        self._kb = ner_knowledge_base.KnowledgeBase("kbstatsshm")
        self.groups = {}
        self.groupsData = {}
        self.isOnline = False
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
        try:
            self._kb.start()
            self._kb.initName_dict()
            self.isOnline = True
        except:
            self.isOnline = False
            raise
        
    def drop(self):
        '''
        Dealocate KB from memory.
        '''
        try:
            self._kb.end()
            self.isOnline = False
        except:
            self.isOnline = False
            raise
        
    
    
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
        return self.isOnline

