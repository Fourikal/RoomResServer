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
|---|---|---|---|
|   |   |   |   |
|list | |building, from, to|list of dictionaries. Every dcitionary consist of the fields to one particular room. last element is a dictionoary that contains type and which client asked|YES|
|bookings|user| |list of dictionaries that contains the information of one particular booking. last element is a dictionoary that contains type and which client asked|YES|
|cardask|user, bookingid|   |confirmed/denied/booked|YES|
|cardCancelRest|user, roomid|   |confirmed|YES (will add checking if time already is expired)|
|makeBooking|User, Room, From, To|  |Confirmed/denied|NO|


