__author__ = 'Anders'
import mqttFields
import databasectrl
import json



class parser:

    def __init__(self):
        self.db=databasectrl.db()

    def sendMessage(self, payload, client):
        clientlist={1: mqttFields.topic2}
        data=json.dumps(payload)
        client.publish(clientlist[1], data)

    def choose(self, innputjson1, client): # Choose method
        if innputjson1['command']=='liste':
            self.sendMessage(self.db.getAvailableRooms(innputjson1), client)
        elif innputjson1['command']=='bookings':
             self.sendMessage(self.db.myBookings(innputjson1), client)
        elif innputjson1['command']=='cardask':
             print("ask")
             self.sendMessage(self.db.cardAsk(innputjson1), client)



    def parsek(self, msg, client):
        if type(json.loads(str(msg.payload)[2:-1])) == dict :
            self.choose(json.loads(str(msg.payload)[2:-1], object_hook=dict), client)
        else:
            pass

