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
|makeBooking|User, Room, From, To|  |Confirmed/denied|NO|



### examples of messages and answers:


```
sent to server:
{'to': 1490976000, 'command': 'liste', 'building': 'Realfagsbygget', 'clientname': 'client1', 'from': 1490972400}
Response:
{'Name': 'R1', 'Id': 2}
{'type': 'list', 'clientname': 'client1'}

sent to server:
{'command': 'liste', 'clientname': 'client1'}
Response:
{'Name': 'R90'}
{'Name': 'R1'}
{'Name': 'El101'}
{'type': 'list', 'clientname': 'client1'}

sent to server:
{'clientname': 'client1', 'command': 'bookings', 'user': 1}
Response:
{'User_Id': 1, 'Confirmed': None, 'FromTimeNumber': 1490947200, 'Room_Position_idPosition': 1, 'Room_Id1': 1, 'ToTimeNumber': 1492283315, 'Id': 1, 'Breached': None}
{'User_Id': 1, 'Confirmed': None, 'FromTimeNumber': 1490947200, 'Room_Position_idPosition': 2, 'Room_Id1': 2, 'ToTimeNumber': 1490954400, 'Id': 2, 'Breached': None}
{'User_Id': 1, 'Confirmed': None, 'FromTimeNumber': 1500648, 'Room_Position_idPosition': 3, 'Room_Id1': 3, 'ToTimeNumber': 1490954400, 'Id': 3, 'Breached': None}
{'type': 'bookinglist', 'clientname': 'client1'}

sent to server:
{'clientname': 'client1', 'command': 'cardCancelRest', 'bookingId': 1, 'user': 1}
Response:
{'type': 'cancelledRest', 'status': 'ok', 'clientname': 'client1'}

sent to server:
{'clientname': 'client1', 'command': 'cardask', 'user': 1, 'roomId': 1}
Response:
{'type': 'cardAsked', 'clientname': 'client1', 'response': 'bookable'}
```