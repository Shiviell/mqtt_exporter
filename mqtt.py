import paho.mqtt.client as mqtt
import json
#import random

broker_address = "swtz-op5"
port = 1883
topic = "$SYS/broker/#"
# Generate a Client ID with the subscribe prefix.
#client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

x = {}

def on_message(client, userdata, message):
    str(message.topic)
    x[str(message.topic)] = message.payload.decode()
    print(str(message.topic).split('/')[:] ," Received message:", message.payload.decode())
    with open('metrics.json', 'w') as json_file:
        try:
            json.dump( x , json_file)
        except Exception as e:
            print(e)
    metric = ''
    #str(message.topic).split('/')[:]
    for i,j in x.items():
        if len(i.split('/')) > 3:
            n = ('_'.join(map(str,i.split('/')[1:-2]))).replace(' ','_')
            metric += '%s{%s="%s"} %s\n' % (n,(i.split('/')[-2]).replace(' ','_'),(i.split('/')[-1]).replace(' ','_'),j)
        else: metric += '%s{%s="%s"} %s\n' % ((i.split('/')[1]).replace(' ','_'),(i.split('/')[-1]).replace(' ','_'),j.replace(' ','_'),'1')

    with open('metrics.txt', 'w') as ffile:
        try:
            #json.dump( x , json_file)
                ffile.write(metric)

        except Exception as e:
            print(e)
    
if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(broker_address, port=port)
    print("Server started http://%s:%s" % (broker_address, port))    
    client.subscribe(topic)
    client.on_message = on_message
    

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass

    client.disconnect()
    print("disconected from mqtt Server .")
    #print (x)





