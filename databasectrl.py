__author__ = 'Anders'
import pymysql
import DBfields

class db():


    def __init__(self):
        self.connection = pymysql.connect(host=DBfields.host,
                                     user=DBfields.user,
                                     password=DBfields.password,
                                     db='roomdb',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)


    def getRommList(self, innputjson):
        try:
            with self.connection.cursor() as cursor:
                if 'building' in innputjson.keys():
                    sql= "SELECT Room.Name, Room.Id FROM Room INNER JOIN position on room.Position_idPosition=position.idPosition inner join building on position.Building_Id=building.Id where building.Name='"+innputjson['building']+"';"
                else:
                    sql = "SELECT Name FROM Room"
                cursor.execute(sql)
                result = cursor.fetchall()
                #print(result) #debug
                return result
        finally:
            pass