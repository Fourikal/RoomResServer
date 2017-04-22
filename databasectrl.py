__author__ = 'Anders'
import datetime
import pymysql
#import DBfields2 as DBfields
import DBfields
import time

experimentmode=True


class db():
    def __init__(self):
        self.connection = pymysql.connect(host=DBfields.host,
                                          user=DBfields.user,
                                          password=DBfields.password,
                                          db=DBfields.dbname,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()


    # This methods uses getroomlist to get a list of rooms, then iterate trhough everyrrom and for every room iterate
    ## for every booing on that room to see if it is overlap. It is not very efficient.
    def getAvailableRooms(self, innputjson):
        print(innputjson)
        if 'building' in innputjson.keys() and 'from' in innputjson.keys() and 'to' in innputjson.keys():
            sql="SELECT * FROM Room WHERE Id NOT IN (SELECT DISTINCT Room_Id1 FROM Booking WHERE FromTimeNumber<='%s' AND ToTimeNumber>='%s');"% (innputjson['to'], innputjson['from'])
            self.cursor.execute(sql)
        elif 'building' in innputjson.keys():
            sql = "SELECT * FROM Room INNER JOIN Position INNER JOIN Building WHERE Building.Name='%s';" % (innputjson['building'])
        else:
            sql = "SELECT * FROM Room"
        self.cursor.execute(sql)
        AvRooms = self.cursor.fetchall()
        AvRooms.append({'type': 'list', 'clientname': innputjson['clientname']})
        return AvRooms

    # myBooking shows every booking for one user.
    def myBookings(self, inputJson):
        #try:
            booking = []
            sql = "SELECT * From Booking where User_Id='%s';" %(str(inputJson['user']))
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for i in result:
                tid1=i['FromTimeNumber']
                tid2=i['ToTimeNumber']
                i['FromTimeNumber']=tid1.strftime('%c')
                i['ToTimeNumber']=tid2.strftime('%c')
                booking.append(i)
            booking.append({'type': 'bookinglist', 'clientname': inputJson['clientname']})
            return booking
        #except:
            #return [{'type': 'error', 'errorMsg': 'mybookings'}]
        #finally:
            #pass

    def RFIDisUser(self, innputjson):
        try:
            sql = "SELECT Id FROM User WHERE RFID='%s';" % (innputjson['RFID'])
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            return [{'type': 'RFIDisUser', 'userId': user['Id'], 'RFID': innputjson['RFID']}] #todo: fix the user id field so its not returned as its own dict
        except:
            return [{'type': 'error', 'errorMsg': 'RFIDisUser'}]
        finally:
            pass

    # This takes in
    def cardAsk(self, innputjson):
        # Is there a booking for that room at this moment?
        # If yes, then is it the same user that queries?
        try:
            if 'user' not in innputjson.keys():
                innputjson['user']=self.RFIDisUser(innputjson)[0]['userId']
            print(innputjson)
            sql="SELECT DISTINCT Room_Id1, User_Id, Id FROM Booking WHERE Room_Id1=%s AND FromTimeNumber<NOW() AND ToTimeNumber>now();" % (innputjson['roomId'])
            self.cursor.execute(sql)
            resset=self.cursor.fetchall()
            verdi=len(resset)
            if verdi==None or verdi==0:
                message = "bookable"
            elif verdi==1:
                if innputjson['user'] == resset[0]['User_Id']:
                    message = "confirmed"
                    sql = "UPDATE Booking SET Confirmed=1 WHERE ID=%s;" % (resset[0]['Id'])
                    self.cursor.execute(sql)
                    self.connection.commit()
                else:
                    message = "busy"
            return [{'type': 'cardAsked', 'clientname': innputjson['clientname'], "response": message}]
        except:
            return [{'type': 'error', 'errorMsg': 'cardAsk'}]
            pass
        finally:
            pass

    def cardCancelRest(self, inputjson):
        # finds booking in database, updates endtime to now
        try:
            sql = "UPDATE Booking SET ToTimeNumber =" + str(int(time.time())) + "  WHERE Id='" + str(
                inputjson['bookingId']) + "'; "
            self.cursor.execute(sql)
            self.connection.commit()
            return [{'type': 'cancelledRest', 'clientname': inputjson['clientname'], 'status': 'ok'}]
        except:
            return [{'type': 'error', 'errorMsg': 'cardCancelrest'}]
            pass
        finally:
            pass

    def makeBooking(self, inputjson):
        try:
            sql = "INSERT INTO Booking (Room_Id1, FromTimeNumber, ToTimeNumber, User_Id) VALUES ('%s', %s, %s, %s ) " % (
            inputjson['roomId'], inputjson['from'], inputjson['to'], inputjson['user'])
            if experimentmode:
                print(sql)
            else:
                self.cursor.execute(sql)
                self.connection.commit()
            return [{'type': 'makeBooking', 'msg': 'Ok'}]
        except:
            return [{'type': 'error', 'errorMsg': 'makeBooking'}]
        finally:
            pass

    def deleteBooking(self, inputjson):
        try:
            sql = "DELETE FROM Booking WHERE Id=%s;" % (inputjson['bookingId'])
            if experimentmode:
                print(sql)
            else:
                self.cursor.execute(sql)
                self.connection.commit()
            return [{'type': 'deleteBooking', 'msg': 'Ok'}]
        except:
            return [{'type': 'error', 'errorMsg': 'deleteBooking'}]
        finally:
            pass

    def addRoom(self, inputjson):
        pass

