from bme_280.bme280 import *
import datetime
import urllib2
import time
import json

# Loading json template to send as a POST request to MongoDB server.
f = open('bme_template.json')
sensor_post = json.loads(f.read())
f.close()

# Continue to read and display temperature, pressure and humidity values to console.
while(True):
    # Grab a tuple that returns temp, pressure and humidity.
    temp, pressure, humidity = readBME280All()

    # Grab current time, and convert to required format.
    utc_time = datetime.datetime.utcnow()
    time_stamp = str(utc_time.strftime("%m.%d.%Y %I:%M %p")) 

    # Parsing values into the json template.
    sensor_post['values'][0]['value'] = temp
    sensor_post['values'][1]['value'] = pressure
    sensor_post['values'][2]['value'] = humidity

    # Parsing timestamps into the json template.
    for sensor_dict in sensor_post['values']:
        sensor_dict['timeStamp'] = time_stamp

    # Printing out json for verification.
    print json.dumps(sensor_post, indent=2)

    # Print out the values from sample.
    print "Temperature : " + str(temp) + " C"
    print "Pressure: " + str(pressure) + " hPa"
    print "Humidity: " + str(humidity) + "%"
    print "--------------------------------------"

    time.sleep(1)

