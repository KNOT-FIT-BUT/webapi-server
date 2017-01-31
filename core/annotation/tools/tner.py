# -*- coding: utf-8 -*-
'''
Created on 24. 4. 2014

@author: casey
'''
import ner
from core.annotation.tools._abstract import AbstractTool
import name_recognizer.name_recognizer as name_recognizer

class NER(AbstractTool):
    '''
    classdocs
    '''
    toolName = "ner"
    params=["lower", "remove_accent"]

    def __init__(self):
        '''
        Constructor
        '''
        super(NER, self).__init__()
        self.require = ['asset', 'input_data']
        self.assetPart = "kb"

    def _hook(self, request):
        request.ongoing_data = self.call(request.input_data, request.asset, request.tool_params)

    def call(self, input_data, asset, params ):
        kb = asset.getPart(self.assetPart)
        ner.dictionary=None
        data = ner.recognize(kb, input_data, False, False, False, params.get("lower", False), params.get("remove accent", False), params.get("name_recognize", False))

        return data
