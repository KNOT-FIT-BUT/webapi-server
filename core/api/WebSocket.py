import cherrypy

from ws4py.websocket import WebSocket

class WebsocketHandler(WebSocket):
    
    def __init__(self,  sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None):
        WebSocket.__init__(self, sock, protocols, extensions, environ, heartbeat_freq)
        self.json_rpc = cherrypy.engine.json_rpc
        
        
    def received_message(self, message):
        """
        Automatically sends back the provided ``message`` to
        its originating endpoint.
        """
        print "ws message accepted"
        print cherrypy.tree.apps[''].config['global']['tools.staticdir.root']
        self.send("accepted", message.is_binary) 
        print self.json_rpc.callRPC("websocket")

    def propagate(self, msg):
        cherrypy.engine.publish('websocket-broadcast', str(msg))
        
        


