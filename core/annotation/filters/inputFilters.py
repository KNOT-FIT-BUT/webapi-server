# -*- coding: utf-8 -*-
'''
Created on 12. 5. 2014

@author: casey
'''
from ner import remove_accent
from core.annotation.filters._abstract import AbstractFilter


class UTFEncode(AbstractFilter):
    
    
    def _hook(self, request):
        request.input_data = self.encode(request.input_data)
        
    def encode(self, text):
        tmptext = self.safe_str(text.encode("utf-8"))
        return tmptext
    
    def safe_unicode(self, obj, *args):
        """ return the unicode representation of obj """
        try:
            return unicode(obj, *args)
        except UnicodeDecodeError:
            # obj is byte string
            ascii_text = str(obj).encode('string_escape')
            return unicode(ascii_text)

    def safe_str(self, obj):
        """ return the byte string representation of obj """
        try:
            return str(obj)
        except UnicodeEncodeError:
            # obj is unicode
            return unicode(obj).encode('unicode_escape')
        

class CharFilter(AbstractFilter):
    
    
    def _hook(self, request):
        request.input_data = self.filter(request.input_data)
        
    def filter(self, text):
        tmptext = text.rstrip() + "\n"
        return tmptext.replace(u"–",u"-").replace(u"“",u' ').replace(u"”",u' ').replace(u"’",u' ').replace(u"‘",u' ').replace(u";",u" ").replace(";"," ")
    
    
class RemoveAccent(AbstractFilter):
    
    def _hook(self, request):
        request.input_data = self.filter(request.input_data)
        
    def filter(self, text):
        return remove_accent(text)
    