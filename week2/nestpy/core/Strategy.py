import json
from pydantic import BaseModel
from .Command import BodyRetrievalCommand, QueryRetrievalCommand, PathRetrievalCommand

def serialize_to_json(data):
    if isinstance(data, list):
        res = [item.dict() for item in data]
        return json.dumps(res)
    if isinstance(data, dict):
        return json.dumps(data)
    if isinstance(data, BaseModel):
        return data.model_dump_json()
    if hasattr(data, 'to_dict'):
        return json.dumps(data.to_dict())
    return json.dumps(data)

# NOTE - Strategy Pattern
class HTTPRequestStrategy:
  def process_request(self, handler, **kwargs):
    pass

class GetStrategy(HTTPRequestStrategy):
  def process_request(self, handler, **kwargs):

    method = handler.map_path_to_method('GET')
    body = BodyRetrievalCommand().execute(handler)
    query = QueryRetrievalCommand().execute(handler)
    path = PathRetrievalCommand().execute(handler)
    
    if method:
      try:
        inputs = handler.map_inputs(method, body, query, path)
        response = method(**inputs)
      except Exception as e:
        handler.send_response(500)
        handler.end_headers()
        handler.wfile.write(str(e).encode('utf-8'))
        return
    else:
      handler.send_response(404)
      handler.end_headers()
      handler.wfile.write(b'Not found')
      return
    
    handler.send_response(200)
    handler.end_headers()
    
    response = serialize_to_json(response)
    if isinstance(response, str):
      response = response.encode('utf-8')
    handler.wfile.write(response)

class PostStrategy(HTTPRequestStrategy):
  def process_request(self, handler, **kwargs):
    method = handler.map_path_to_method('POST')
    body = BodyRetrievalCommand().execute(handler)
    query = QueryRetrievalCommand().execute(handler)
    path = PathRetrievalCommand().execute(handler)

    if method:
      try:
        inputs = handler.map_inputs(method, body, query, path)
        response = method(**inputs)
      except Exception as e:
        handler.send_response(500)
        handler.end_headers()
        handler.wfile.write(str(e).encode('utf-8'))
        return
    else:
      handler.send_response(404)
      handler.end_headers()
      handler.wfile.write(b'Not found')
      return

    handler.send_response(201)
    handler.end_headers()

    response = serialize_to_json(response)
    if isinstance(response, str):
      response = response.encode('utf-8')
    handler.wfile.write(response)