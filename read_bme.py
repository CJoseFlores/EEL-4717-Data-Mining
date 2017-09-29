from collections import OrderedDict
from datetime import datetime
from bme_280.bme280 import *
import pendulum
import urllib2
import time
import json
import ssl

# Loading json template to send as a POST request to MongoDB server.
f = open('bme_template.json')
sensor_post = json.loads(f.read(), object_pairs_hook=OrderedDict)
f.close()

# Continue to read and display temperature, pressure and humidity values to console.
while(True):
    # Grab a tuple that returns temp, pressure and humidity.
    temp, pressure, humidity = readBME280All()

    # Grab current time in EST, and convert to required format.
    us_eastern = pendulum.timezone('US/Eastern')
    local_time = datetime.now(us_eastern)
    time_stamp = str(local_time.strftime("%m.%d.%Y %I:%M %p")) 

    # Parsing values into the json template.
    sensor_post['values'][0]['value'] = temp
    sensor_post['values'][1]['value'] = pressure
    sensor_post['values'][2]['value'] = humidity

    # Parsing timestamps into the json template.
    for sensor_dict in sensor_post['values']:
        sensor_dict['timeStamp'] = time_stamp

    # Printing out json for verification.
    print json.dumps(sensor_post, indent=2)
    f = open('sample_output.json', 'w')
    f.write(json.dumps(sensor_post, indent=2))
    f.close()

    # Sending out formatted json to MongoDB server, and print response.
    req = urllib2.Request(url="https://10.109.143.88:8443/sendsensorvalue/", data=json.dumps(sensor_post),
            headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}) 
    context = ssl._create_unverified_context()
    open_url = urllib2.urlopen(req, context=context)
    response = open_url.read()
    
    print json.dumps(response, indent=2)

    # Print out the values from sample.
    print "Temperature : " + str(temp) + " C"
    print "Pressure: " + str(pressure) + " hPa"
    print "Humidity: " + str(humidity) + "%"
    print "--------------------------------------"

    time.sleep(5)

