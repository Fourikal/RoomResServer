__author__ = 'Anders'
import pymysql
import DBfields
import time


def checkTimeOverlap(intervallA, intervallB):
    return max(0, min(intervallA[1], intervallB[1]) - max(intervallA[0], intervallB[0]))


class db():
    def __init__(self):
        self.connection = pymysql.connect(host=DBfields.host,
                                          user=DBfields.user,
                                          password=DBfields.password,
                                          db=DBfields.dbname,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def getRommList(self, innputjson):
        # Gets list of rooms (Performance-warning: This is primarily its own method for reuse-purposes in other methods)
        try:
            if 'building' in innputjson.keys():
                sql = "SELECT Room.Name, Room.Id FROM Room INNER JOIN Position on Room.Position_idPosition=Position.idPosition inner join Building on Position.Building_Id=Building.Id where Building.Name='" + \
                      innputjson['building'] + "';"
            else:
                sql = "SELECT Name FROM Room"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            # print(result) #debug
            return result
        finally:
            pass

    def getAvailableRooms(self, innputjson):
        # This method gets rooms. Optional filters: buidling, time which it is free. AvRooms contains roomname and id for rooms that fullfills the demands
        allRooms = self.getRommList(innputjson)
        AvRooms = []
        if 'from' in innputjson.keys() and 'to' in innputjson.keys():
            for i in allRooms:
                flag = True
                try:
                    sql = "SELECT * FROM Booking where Room_ID1='" + str(i['Id']) + "'"
                    self.cursor.execute(sql)
                    allBookingsPerRoom = self.cursor.fetchall()
                    for j in allBookingsPerRoom:
                        if checkTimeOverlap([j['FromTimeNumber'], j['ToTimeNumber']],
                                            [innputjson['from'], innputjson['to']]) != 0:
                            flag = False
                    if flag == True:
                        AvRooms.append(i)
                finally:
                    pass
        else:
            AvRooms = allRooms
        AvRooms.append({'type': 'list', 'clientname': innputjson['clientname']})
        return AvRooms

    def myBookings(self, inputJson):
        try:
            sql = "SELECT * From Booking where User_Id='" + str(inputJson['user']) + "';"
            self.cursor.execute(sql)
            booking = self.cursor.fetchall()
            booking.append({'type': 'bookinglist', 'clientname': inputJson['clientname']})
            return booking
        finally:
            pass

    def cardAsk(self, innputjson):
        # Is there a booking for that room at this moment?
        # If yes, then is it the same user that queries?
        flag = True
        try:
            sql = "SELECT * FROM Booking where Room_ID1='" + str(innputjson['roomId']) + "'"
            self.cursor.execute(sql)
            allBookingsPerRoom = self.cursor.fetchall()
            for j in allBookingsPerRoom:
                tid = int(time.time())
                print([j['FromTimeNumber'], j['ToTimeNumber']], [tid, tid + 5])
                if checkTimeOverlap([j['FromTimeNumber'], j['ToTimeNumber']], [tid, tid + 5]) != 0:
                    flag = False
                    if innputjson['user'] == j['User_Id']:
                        message = "confirmed"
                    else:
                        message = "busy"
            if flag == True:  # todo everything here must 'ordnes med'
                message = "bookable"
                print("ledig")
            return [{"response": message}, {'type': 'cardAsked', 'clientname': innputjson['clientname']}]
        except:
            pass
        finally:
            pass
