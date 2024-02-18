import json
import urllib.parse

class RetrievalCommand(object):
    def execute(self, handler):
        self.action(handler)


class BodyRetrievalCommand(RetrievalCommand):
    def execute(self, handler):
        content_length = handler.headers['Content-Length']
        if (content_length is None):
            return {}
        body = handler.rfile.read(int(content_length))
        return json.loads(body)

  
class QueryRetrievalCommand(RetrievalCommand):
    def execute(self, handler):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(handler.path).query)
        return query
    
class PathRetrievalCommand(RetrievalCommand):
    def execute(self, handler):
        parsed_path = urllib.parse.urlparse(handler.path)
        path = parsed_path.path.strip('/')
        if path == '':
            return ''
        
        return path
