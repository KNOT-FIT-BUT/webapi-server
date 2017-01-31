import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import cherrypy
import os

from core.web import Root
from core.core import AppCore
from core.api.WebSocket import WebsocketHandler
from core.api.REST import RESTHandler
from core.api.HTTP import HTTPHandler
from core.api.JSONRPC import JSONRPCHanlder

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from cherrypy.process.plugins import PIDFile

current_dir = os.path.dirname(os.path.abspath(__file__))


def main():
    #cherrypy.config.update({'error_page.404': error_page_404})
    cherrypy.config.update('webapiner.ini')
    print cherrypy.__version__
    core = AppCore()
    
    WebSocketPlugin(cherrypy.engine).subscribe()
    
    cherrypy.engine.json_rpc = JSONRPCHanlder(cherrypy.engine, core)
    cherrypy.engine.json_rpc.subscribe()
    
    cherrypy.tools.websocket = WebSocketTool()
    
    http_conf = {
                 '/':{'tools.staticdir.on':False}
                 }
    
    rest_conf = {
                 '/':{'request.dispatch':cherrypy.dispatch.MethodDispatcher()}
                 }
    
   
    
    cherrypy.tree.mount(RESTHandler(), "/api/REST/", config = rest_conf)
    cherrypy.tree.mount(HTTPHandler(), "/api/HTTP/", config = http_conf)
    
    
    
    PIDFile(cherrypy.engine, os.path.join(current_dir, "webapiner.pid")).subscribe()
    cherrypy.engine.subscribe("start", core.inito)
    cherrypy.engine.subscribe("stop", core.destroy)
    cherrypy.quickstart(Root(),'/','webapiner.ini')

    
    
if __name__ == '__main__':
    main()    
    
