'''
Created on 24. 4. 2014

@author: casey
'''

class Pipeline(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.data = {}
        self.nextHandler = None

    def __add__(self, newHandler):
        """Used to append handlers to each other"""
        if not isinstance(newHandler, Pipeline):
            raise TypeError('Handler.__add__() expects Pipeline')
        if self.nextHandler:
            self.nextHandler + newHandler
        else:
            self.nextHandler = newHandler
            while newHandler:
                newHandler.data = self.data
                newHandler = newHandler.nextHandler
        return self

    def process(self, request):
        """Wrapper around the internal _hook method"""
        self._hook(request)
        if self.nextHandler:
            return self.nextHandler.process(request)
        else:
            self.data.clear( )
        return

    def _hook(self, request):
        """Default hook method to be overridden in subclasses"""
        return True
    

