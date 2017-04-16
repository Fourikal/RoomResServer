# RoomResServer

## Protocol and payload
We are using the MQTT-protocol or communication. See the [mqttfields document](mqttFields.py) for information to connect with the at any time used mqtt broker. As library for
mqtt communication in Python i have used the Paho-mqtt library. This is installed in the following way with pip.

```
pip install paho-mqtt
```

When installing for python3.x and having other python versions on your system i think you will have to use the following piece of code instead. (Do not know how things work, just push buttons until things work

```
pip3 install paho-mqtt
```

## Database

Standard mysql database, se [database fields document](DBfields.py) for information on how to connect with the database.
Using pymysql.

to install on python

```
pip install pymysql
```

## Message types

### Overview

|Command|mandatory parameters|optional parameters|output|implemented|
|---|---|---|---|---|
|list | |building, from, to|list of dictionaries. Every dcitionary consist of the fields to one particular room. last element is a dictionoary that contains type and which client asked|YES|
|bookings|user| |list of dictionaries that contains the information of one particular booking. last element is a dictionoary that contains type and which client asked|YES|
|cardask|user, bookingid|   |confirmed/denied/booked|YES|
|cardCancelRest|user, roomid|   |confirmed|YES (will add checking if time already is expired)|
|makeBooking|User, Room, From, To|  |Confirmed/denied|YES|
|deleteBooking|bookingId|   |Confirmed|YES|
|RFIDisUser|RFID|  |UserId|YES|



### examples of messages and answers:


```
{'building': 'Realfagsbygget', 'clientname': 'client1', 'to': 1490976000, 'from': 1490972400, 'command': 'liste'}
Response:
{'Id': 2, 'Name': 'R1'}
{'clientname': 'client1', 'type': 'list'}

sent to server:
{'clientname': 'client1', 'command': 'liste'}
Response:
{'Name': 'R90'}
{'Name': 'R1'}
{'Name': 'El101'}
{'clientname': 'client1', 'type': 'list'}

sent to server:
{'clientname': 'client1', 'user': 1, 'command': 'bookings'}
Response:
{'Id': 1, 'Room_Position_idPosition': 1, 'Confirmed': 0, 'FromTimeNumber': 1490947200, 'Breached': 0, 'ToTimeNumber': 1492367449, 'User_Id': 1, 'Room_Id1': 1}
{'Id': 2, 'Room_Position_idPosition': 2, 'Confirmed': 0, 'FromTimeNumber': 1490947200, 'Breached': 0, 'ToTimeNumber': 1490954400, 'User_Id': 1, 'Room_Id1': 2}
{'Id': 3, 'Room_Position_idPosition': 3, 'Confirmed': 0, 'FromTimeNumber': 1500648, 'Breached': 0, 'ToTimeNumber': 1490954400, 'User_Id': 1, 'Room_Id1': 3}
{'Id': 4, 'Room_Position_idPosition': 1, 'Confirmed': 0, 'FromTimeNumber': 1491473600, 'Breached': 0, 'ToTimeNumber': 1491625200, 'User_Id': 1, 'Room_Id1': 1}
{'clientname': 'client1', 'type': 'bookinglist'}

sent to server:
{'clientname': 'client1', 'bookingId': 1, 'user': 1, 'command': 'cardCancelRest'}
Response:
{'clientname': 'client1', 'status': 'ok', 'type': 'cancelledRest'}

sent to server:
{'roomId': 1, 'RFID': 'abab', 'user': 1, 'command': 'cardask', 'clientname': 'client1'}
Response:
{'clientname': 'client1', 'response': 'bookable', 'type': 'cardAsked'}

sent to server:
{'command': 'makeBooking', 'roomId': 1, 'user': 1, 'clientname': 'client1', 'to': 400, 'from': 200}
Response:
{'msg': 'Ok', 'type': 'makeBooking'}

sent to server:
{'clientname': 'client1', 'bookingId': 7, 'user': 1, 'command': 'deleteBooking'}
Response:
{'msg': 'Ok', 'type': 'deleteBooking'}

sent to server:
{'clientname': 'client1', 'RFID': 'abab', 'command': 'RFIDisUser'}
Response:
{'userId': {'Id': 1}, 'RFID': 'abab', 'type': 'RFIDisUser'}
```