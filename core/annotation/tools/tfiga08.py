import re
#import figa.sources.marker as figa
try:
    import figav08.figa.marker as figa
except:
    pass

from core.annotation.tools._abstract import AbstractTool



class Figa08(AbstractTool):
    
    toolName = "figa08"
    
    def __init__(self):
        super(Figa08, self).__init__()
        self.require = ['asset','input_data']
        self.assetPart = "fsa"
        
    def _hook(self, request):
        request.ongoing_data = self.call(request.input_data, request.asset)
    
    def call(self, input_data, asset):
        fsa = asset.getPart(self.assetPart)
        dictionary = figa.myList()
        lang_file = None
        dictionary.insert(fsa.getTargetPath().encode("utf-8"))
        seek_names = figa.marker(dictionary, lang_file)
        output = seek_names.lookup_string(input_data.encode("utf-8"))
        return self.parse(output) 
    
    
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
                                       new_entities[-1].end) != 0:
                    new_entities.append(ent)
                else:
                    pass
            
            entities = new_entities
        return entities
    
class SimpleEntity():
    
    """A text entity refering to a knowledge base item."""
    
    def __init__(self, entity_str):

        """
        Create an entity by parsing a line of figa output from entity_str. 
        Entity will be referring to an item of an knowledge base object kb.
        """

        entity_attributes = entity_str.split('\t')
        self.senses = []
        for sense in entity_attributes[0].split(';'):
            #sense 0 marks a coreference
            if sense != '0':
                self.senses.append(int(sense))
        #start offset is indexed differntly from figa
        self.begin = int(entity_attributes[1]) - 1
        self.start_offset = self.begin
        self.end_offset = int(entity_attributes[2])
        self.source = entity_attributes[3]
        #convert utf codes
        self.source = re.sub("&#x([A-F0-9]{2});","\\x\g<1>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>\\x\g<4>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>\\x\g<4>\\x\g<5>", self.source)
        self.source = re.sub("&#x([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2})([A-F0-9]{2});","\\x\g<1>\\x\g<2>\\x\g<3>\\x\g<4>\\x\g<5>\\x\g<6>", self.source)
        self.source = eval("\"" + self.source + "\"")
        self.preferred_sense = self.senses[0] if len(self.senses)> 0 else None
        
    
    def mutual_position (self, begin_offset, end_offset):
        """
        Evaluates mutual position in a source text of self and a entity starting
        at begin_offset and ending at end_offset. If self stands entirely before
        the other entity returns -1. If entities overlap, returns 0. If self 
        stands entirely after the other entity, returns 1.
        """
        if int(self.end_offset) < int(begin_offset):
            return -1
        elif int(self.begin) > int(end_offset):
            return 1
        else:
            return 0
        
    def is_coreference(self):
        return False

    def get_preferred_sense(self):
        return self.senses[0]