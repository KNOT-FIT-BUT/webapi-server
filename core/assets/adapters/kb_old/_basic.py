import gc
import commands
import os
from ctypes import cdll, POINTER, c_char_p, c_int, c_void_p


from abstract import KnowledgeBaseAdapter

class KB_Basic(KnowledgeBaseAdapter):
    '''
    Simple KB container for NON NER USAGE!
    '''
    
    
    def __init__(self, base_folder, kb_path):
        super(KB_Basic, self).__init__(base_folder, kb_path)
        self.lines = None

        
        
    
    def _load(self):
        '''
        Load KB from file via kb_loader.so.
        '''
        count = commands.getoutput('wc -l ' + self.kb_path + ' | cut -d" " -f1')
        print self.kb_path, self.base_folder
        self.items_number = int(count)
        maxitem = 33 
        lib = cdll.LoadLibrary( os.path.join(self.base_folder, "api","NER","figav08","figa","kb_loader.so"))
        lib.queryTree.restype = POINTER(POINTER(c_char_p))
        lib.queryTree.argtypes = [c_char_p,c_int,c_int]

        self.lines = lib.queryTree(self.kb_path, self.items_number, maxitem);
        #time.sleep(5)
        self.status = KB_Basic.LOADED
    
    


    
    
        
 
    
    