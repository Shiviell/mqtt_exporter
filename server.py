# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
#import time

hostName = "0.0.0.0"
serverPort = 9080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print (self.path)
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header("Content-type", "text/plain; version=0.0.4; charset=utf-8")
            self.end_headers()
            #self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            with open('metrics.txt', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
        elif self.path == '/favicon.ico':
            self.send_response(200)
            self.send_header("Content-type", "image/x-icon")
            self.end_headers()
            with open('favicon.ico', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
            
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('defult.html', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
