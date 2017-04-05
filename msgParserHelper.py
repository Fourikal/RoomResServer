__author__ = 'Anders'
import databasectrl
import json

db=databasectrl.db()
def sendMessage(payload, client):
    clientlist={1: '/hopp/ned/2'}
    data=json.dumps(payload)
    client.publish(clientlist[1], data)

def choose(command, innputjson ,client): # Choose method
    metoder={'list': db.getAvailableRooms(innputjson),'bookings': db.myBookings(innputjson)}
    #metoder={'list': db.getAvailableRooms(innputjson)}
    data=metoder[command]
    sendMessage(data, client)

def parse(msg, client):
    innputjson=json.loads(str(msg.payload)[2:-1])
    #print(innputjson['command']) #debug
    return choose(innputjson['command'], innputjson, client)

