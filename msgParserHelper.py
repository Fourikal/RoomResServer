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
        return

    def choose(self, innputjson1, client): # Choose method
        try:
            if innputjson1['command']=='liste':
                self.sendMessage(self.db.getAvailableRooms(innputjson1), client)
            elif innputjson1['command']=='bookings':
                 self.sendMessage(self.db.myBookings(innputjson1), client)
            elif innputjson1['command']=='cardask':
                 self.sendMessage(self.db.cardAsk(innputjson1), client)
            elif innputjson1['command']=='cardCancelRest':
                 self.sendMessage(self.db.cardCancelRest(innputjson1), client)
            elif innputjson1['command']=='makeBooking':
                 self.sendMessage(self.db.makeBooking(innputjson1), client)
            elif innputjson1['command']=='deleteBooking':
                 self.sendMessage(self.db.deleteBooking(innputjson1), client)
            elif innputjson1['command']=='RFIDisUser':
                self.sendMessage(self.db.RFIDisUser(innputjson1), client)
        except:
            pass


    def parsek(self, msg, client):
        if type(json.loads(str(msg.payload)[2:-1])) == dict :
            self.choose(json.loads(str(msg.payload)[2:-1], object_hook=dict), client)
        else:
            pass

