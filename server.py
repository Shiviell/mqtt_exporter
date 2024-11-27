# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
#import yaml
import json
#import time
import subprocess
import glob
import urllib.parse

hostName = "0.0.0.0"
serverPort = 9502

def prom_exporter (module,target,slaveID,byteOrder):
    metric = ""
    try:
        files = glob.glob('./reg/%s*.modbus' % (module))
        if len(files) == 0 :
            raise ValueError("Missing 'module file' in payload")
        for file in files:
            # Extract the command from the payload
            command = "modbus -r %s -s %i -B %s %s \* -t 1" % (file,int(slaveID),byteOrder,target,)
            # Execute the command
            print (command)
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            a = result.stdout.split('\n')
            for line in a:
                b = line.strip().split(': ')
                if len(b) == 2 : 
                    c = b[0].split('_')
                    try:
                        metric += '%s{IO="%s",address="%s",cell="%i"} %s\n' % ('_'.join(c[2:-1]),c[1],c[0],int(c[-1]),b[1])
                    except:
                        metric += '%s{IO="%s",address="%s"} %s\n' % ('_'.join(c[2:]),c[1],c[0],b[1])
        return metric
    except Exception as e: return str(e)

                    

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        #print (self.path)
        try:
            if self.path.split("?")[0] == '/metrics':
                        # Parse the URL to extract the query string
                url_parts = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(url_parts.query)
                metrics = prom_exporter (query_params['module'][-1],query_params['target'][-1],query_params['sub_target'][-1],query_params['byteOrder'][-1])
                self.send_response(200)
                self.send_header("Content-type", "text/plain; version=0.0.4; charset=utf-8")
                self.end_headers()
                #self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
                #with open('metrics.txt', 'rb') as file: 
                #    self.wfile.write(file.read()) # Read the file and send the contents 
                self.wfile.write(metrics.encode()) # Read the file and send the contents 
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
        except Exception as e:
            # Handle errors and send an error response
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    def do_POST(self):
        try:
            # Get the content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the payload
            post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
            
            # Parse JSON payload
            params = json.loads(post_data.decode('utf-8'))
            
            # Extract the command from the payload
            command = "modbus -s %i -B %s %s %s -t 1" % (params['slaveID'],params['byteOrder'], params['target'], ' '.join(params['access']))
            if not command:
                raise ValueError("Missing 'command' in payload")
            
            # Execute the command
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Prepare the response
            response = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
            # Send the response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        except Exception as e:
            # Handle errors and send an error response
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))


if __name__ == "__main__":
 
    
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
