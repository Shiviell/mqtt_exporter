# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import time


hostName = "0.0.0.0"
serverPort = 9080
LOKI_URL = "http://100.112.56.97:3100/loki/api/v1/push" #"http://loki:3100/loki/api/v1/push"  # Change this to your Loki URL

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
    def do_POST(self):
        if self.path == '/alertmanager':
            # Read the content length and the body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse the JSON data from Alertmanager
            try:
                alert_data = json.loads(post_data)
                self.process_alerts(alert_data)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Alerts received and processed")
            except Exception as e:
                print(f"Error processing alerts: {e}")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error processing alerts")
        else:
            print(f"Error worng path")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Error on path")
            

    def process_alerts(self, alert_data):
        #reset metric feild
        metric = ''
        # Prepare and send a log entry for each alert
        for alert in alert_data.get("alerts", []):
            #print (alert)
            labels = alert.get("labels", {})
            # add active alarm to metric
            if alert['status'] != 'resolved': metric += 'ALERT%s 1 \n' % (json.dumps(labels))
            labels['status'] = alert['status']
            annotations = alert.get("annotations", {})
            
            # Create a log entry with all labels and annotations
            log_entry = {
                "streams": [
                    {
                        "stream": labels,  # Use all labels directly
                        "values": [
                            [str(int(time.time() * 1_000_000_000)), json.dumps(annotations)]  # Send annotations as log message
                        ],
                    }
                ]
            }
            print (log_entry)

            # Send the log entry to Loki

            try:
                response = requests.post(LOKI_URL, json=log_entry)
                response.raise_for_status()
                print(f"Log for alert '{labels.get('alertname')}' sent to Loki successfully")
            except Exception as e:
                print(f"Failed to send log to Loki: {e}")
        #write to file metrics
        with open('metrics.txt', 'w') as ffile:
            try:
                #json.dump( x , json_file)
                    ffile.write(metric)

            except Exception as e:
                print(f"Failed to open metric file: {e}")
        
                


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
