import subprocess, os, re
import figa.sources.marker as figa

from core.annotation.tools._abstract import AbstractTool
from core.annotation.tools.tfiga08 import SimpleEntity
from figa.autocomplete import autocomplete

class Figa(AbstractTool):
    
    toolName = "figa"
    params=["lower", "remove_accent"]
    
    def __init__(self):
        super(Figa, self).__init__()
        self.require = ['asset','input_data']
        self.assetPart = "fsa"
        
    def _hook(self, request):
        request.ongoing_data = self.call(request.input_data, request.asset, request.tool_params)
    
    def call(self, input_data, asset, params, parse=True):
        fsa = asset.getPart(self.assetPart)
        dictionary = figa.myList()
        lang_file = None
        dictionary.insert(fsa.getTargetPath().encode("utf-8"))
        seek_names = figa.marker(dictionary, lang_file, False, params["overlapping"], params["boundary"])
        output = seek_names.lookup_string(input_data.encode("utf-8"))
        if parse:
            return self.parse(output) 
        else:
            return output
    
    def call_raw(self, input_data, asset_path):
        dictionary = figa.myList()
        lang_file = None
        dictionary.insert(asset_path.encode("utf-8"))
        seek_names = figa.marker(dictionary, lang_file, False, False, False)
        output = seek_names.lookup_string(input_data.encode("utf-8"))
        return output

    def autocomplete(self, input_data,automat, lines):
        #input_data=remove_accent(input_data.lower())
        
        dictionary = figa.myList()
        lang_file = None
        return_all = True if len(input_data.strip()) >= 3 else False
        dictionary.insert(automat.encode("utf-8"))
        output = autocomplete(dictionary, input_data, 10, True, True, lang_file, return_all)
        #seek_names = figa.marker(dictionary, lang_file)
        #output = seek_names.auto_lookup_string(input_data.encode("utf-8"), lines)
        return self.parseAutocomplete(output)
    

    def parse(self, output):
        entities = []
        for line in output.split("\n")[:-1]:
            se = SimpleEntity(line)
            if se.preferred_sense is not None:
                entities.append(se)
        if len(entities) > 0:
            new_entities = [entities[0]]
            for ent in entities:
                if ent.mutual_position(new_entities[-1].begin,
                                       new_entities[-1].end_offset) != 0:
                    new_entities.append(ent)
                else:
                    pass
            
            entities = new_entities
        return entities
    
    def parseAutocomplete(self, output):
        entities = set([])
        for line in output.split("\n")[:-1]:
            #se = AutocompleteEntity(line)
            entities.update([int(a) for a in line.split('\t')[1].split(';')])
            #if se.preferred_sense is not None:
            #    entities.append(se)
        return entities
                
class AutocompleteEntity:
    def __init__(self, entity_str):

        entity_attributes = entity_str.split('\t')
        self.senses = []
        for sense in entity_attributes[1].split(';'):
            #sense 0 marks a coreference
            if sense != '0':
                self.senses.append(int(sense))
        self.source = entity_attributes[0]
        #convert utf codes
        self.source = re.sub("&#x([A-F0-9]{2});","\\x\g<1>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>\\x\g<4>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>\\x\g<4>\\x\g<5>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>\\x\g<4>\\x\g<5>\\x\g<6>", self.source)
        self.source = eval("\"" + self.source + "\"")
        self.preferred_sense = self.senses[0] if len(self.senses)> 0 else None