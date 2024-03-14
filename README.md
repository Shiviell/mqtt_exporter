# mqtt_exporter
minimal eclipse-mosquitto exporter


mqtt.py connect to mqtt broker and update text file metrics.txt.
server.py is a basic httpserver that show metrics.txt on /metrics endpoint.
all is pack in supervisord.conf and run with dockerfile 
