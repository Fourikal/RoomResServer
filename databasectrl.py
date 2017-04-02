__author__ = 'Anders'
import pymysql

class db():


    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='1234',
                                     db='roomdb',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)


    def getRommList(self, innputjson):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT Name FROM Room"
                cursor.execute(sql)
                result = cursor.fetchall()
                #print(result) #debug
                return result
        finally:
            pass