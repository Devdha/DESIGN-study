class HTTPRequestStrategy:
  def process_request(self, handler, **kwargs):
    pass

class GetStrategy(HTTPRequestStrategy):
  def process_request(self, handler, **kwargs):
    method = handler.map_path_to_method('GET')
    body = handler.get_body()
    query = handler.get_query_params()
    path = handler.get_path_params()
    
    if method:
      response = method(**body, **query, **path)
    else:
      handler.send_response(404)
      handler.end_headers()
      handler.wfile.write(b'Not found')
      return
    
    handler.send_response(200)
    handler.end_headers()
    
    response = handler.serialize_to_json(response)
    handler.wfile.write(response.encode('utf-8'))

class PostStrategy(HTTPRequestStrategy):
  def process_request(self, handler, **kwargs):
    method = handler.map_path_to_method('POST')
    body = handler.get_body()
    query = handler.get_query_params()
    path = handler.get_path_params()
    
    if method:
      response = method()
    else:
      handler.send_response(404)
      handler.end_headers()
      handler.wfile.write(b'Not found')
    handler.send_response(200)
    handler.end_headers()
    response = handler.serialize_to_json(response)
    handler.wfile.write(response)