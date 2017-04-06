__author__ = 'Anders'
import msgParserHelper
import databasectrl

verdi1=10
verdi2=20

msgParserHelper.parse({'command': 'list', 'building': 'Realfagsbygget', 'from' : verdi1 , 'to' : verdi2, 'user': 1}, verdi1)