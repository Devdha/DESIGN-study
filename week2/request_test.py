
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import requests
import time

from cats.module import CatsModule
from nestpy.core import NestFactory


def run_server():
    app = NestFactory.create(CatsModule)
    app.serve()

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)

    # List cat test
    response = requests.get('http://localhost:3001')
    print(response.json())

    # Create cat test
    response = requests.post('http://localhost:3001', json={
        "id": "3",
        "name": "Kitty",
        "gender": "F"
      }
    )
    print(response.json())

    # Get cat test
    response = requests.get('http://localhost:3001/3')
    print(response.json())
    
