from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os
import requests
import json

hostName = "localhost"
serverPort = 8080


class MiServidor(BaseHTTPRequestHandler):
    def do_GET(self):
        ##para manejar el path, y poder obtener el id enviado como parametro
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)
        
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            with open('index.html', 'r') as f:
                html = f.read()
            
            self.wfile.write(bytes(html, "utf8"))
        
        elif self.path == "/test":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes(
                    "<html><head><title>https://pythonbasics.org</title></head>"
                    f"<p>Request: {self.path}</p>"
                    "<body><p>This is a test page.</p></body></html>",
                    "utf-8",
                )
            )
        elif self.path == "/post":
            response = requests.get('https://jsonplaceholder.typicode.com/posts')
            posts = response.json()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(posts), "utf-8"))
        
        elif self.path == "/comments":
            response = requests.get('https://jsonplaceholder.typicode.com/comments')
            posts = response.json()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(posts), "utf-8"))
        
        elif self.path == "/albums":
            response = requests.get('https://jsonplaceholder.typicode.com/albums')
            posts = response.json()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(posts), "utf-8"))
        
        elif self.path == "/photos":
            response = requests.get('https://jsonplaceholder.typicode.com/photos')
            posts = response.json()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(posts), "utf-8"))
        
        elif self.path == "/todos":
            response = requests.get('https://jsonplaceholder.typicode.com/todos')
            posts = response.json()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(posts), "utf-8"))
        
        elif path == "/users":
            userId = params.get('userId', [None])[0]

            if userId is not None:
                # Aca obtenemos un usuario específico
                response = requests.get(f'https://jsonplaceholder.typicode.com/users/{userId}')    
            else:
                # Traer todos los usuario
                response = requests.get('https://jsonplaceholder.typicode.com/users')    
               
            posts = response.json()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(posts), "utf-8"))

        elif self.path.endswith(".js"):
            script_path = self.path[1:]  # borra el  "/"
            script_path = os.path.join(os.path.dirname(__file__), script_path)
            if os.path.isfile(script_path):
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.end_headers()

                with open(script_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        
            
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MiServidor)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Servidor stopeado!! :)")
