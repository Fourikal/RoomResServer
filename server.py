__author__ = 'Anders'
import msgParserHelper
import paho.mqtt.client as mqtt
#This file is the communication, it subscribes to a mqtt topic, and on receiving a message it sends it to the helper class.
#Then it gets an approipate response from the helper class and sends it to another topic. It is not very complex, complicated or robust.
#The msgparserhelper does parse. the databasectrl contains every method for database interaction
def on_connect(client, userdata, flags, rc):
    print(("connected with result code "+str(rc)))
    client.subscribe("/hopp/ned")
def on_message(client, userdata, msg):
    msgParserHelper.parse(msg, client)
client=mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)
client.loop_forever()