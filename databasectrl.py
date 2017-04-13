__author__ = 'Anders'
import pymysql
#import DBfields
import DBfields2 as DBfields
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

    #getRommList does return list of rooms in a building or everyone
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
        except:
            pass
        finally:
            pass

    #This methods uses getroomlist to get a list of rooms, then iterate trhough everyrrom and for every room iterate
    ## for every booing on that room to see if it is overlap. It is not very efficient.
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
                except:
                    return [{'type': 'error', 'errorMsg': 'getAvaiRooms'}]
                finally:
                    pass
        else:
            AvRooms = allRooms
        AvRooms.append({'type': 'list', 'clientname': innputjson['clientname']})
        return AvRooms

    #myBooking shows every booking for one user.
    def myBookings(self, inputJson):
        try:
            booking=[] #added this for the null cases
            sql = "SELECT * From Booking where User_Id='" + str(inputJson['user']) + "';"
            self.cursor.execute(sql)
            booking = self.cursor.fetchall()
            if booking==None:
                booking=[]
            booking.append({'type': 'bookinglist', 'clientname': inputJson['clientname']})
            return booking
        except:
            return [{'type': 'error', 'errorMsg': 'mybookings'}]
        finally:
            pass

    #This takes in
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
            return [{'type': 'cardAsked', 'clientname': innputjson['clientname'], "response": message}]
        except:
            return [{'type': 'error', 'errorMsg': 'cardAsk'}]
            pass
        finally:
            pass

    def cardCancelRest(self, inputjson):
        #finds booking in database, updates endtime to now
        try:
            sql="UPDATE Booking SET ToTimeNumber ="+str(int(time.time()))+"  WHERE Id='"+str(inputjson['bookingId'])+"'; "
            self.cursor.execute(sql)
            self.connection.commit()
            return [{'type': 'cancelledRest', 'clientname': inputjson['clientname'], 'status': 'ok'}]
        except:
            return [{'type': 'error', 'errorMsg': 'cardCancelrest'}]
            pass
        finally:
            pass

    def makeBooking(self, inputjson):
        sql= "insert into"
