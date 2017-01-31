'''
Created on 11. 5. 2014

@author: casey
'''
from core.annotation.generators._abstract import AbstractGenerator
import genkit.v1
import genkit.v2

class FigaNer(AbstractGenerator):
    
    def _hook(self, request):
        request.output_data = self.generate(request, request.version)
    
    def generate(self, request, version):
        return getattr(self, '_' + self.__class__.__name__+"__genV"+str(version))(request)
    
    
    def __genV1(self, request):
        return genkit.v1.generate(request.ongoing_data, request.asset.getPart("kb"), True)
    
    
    def __genV2(self, request):
        return genkit.v2.generate(request)