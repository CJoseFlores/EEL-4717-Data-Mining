from collections import OrderedDict
from datetime import datetime
from bme_280.bme280 import *
import pendulum
import requests
import time
import json
import ssl

# Loading json template to send as a POST request to MongoDB server.
f = open('bme_template.json')
sensor_post = json.loads(f.read(), object_pairs_hook=OrderedDict)
#sensor_post = json.loads(f.read())
f.close()

# URL and Header used for HTTP PUT requests.
url = "https://10.109.143.88:8443/sendsensorvalue/"
headers = {"content-type" : "application/json"}
#data = {
#     "pantherId":5160328,
#     "values":[
#         {
#             "variableName":"Temperature",
#             "timeStamp":"09.25.2017 2:37 AM",
#             "value": 23.45
#         },
#         {
#             "variableName":"Pressure",
#             "timeStamp":"09.25.2017 2:37 AM",
#             "value": 1012.087435
#         },
#         {
#             "variableName":"Humidity",
#             "timeStamp":"09.25.2017 2:37 AM",
#             "value": 49.6455102
#         }
#     ]
#}
#   

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
    print sensor_post
    print json.dumps(sensor_post, indent=2)
    f = open('sample_output.json', 'w')
    f.write(json.dumps(sensor_post, indent=2))
    f.close()

    # Sending out formatted json to MongoDB server, and print response.
    try:
        req = requests.put(url, headers=headers, data=json.dumps(sensor_post), verify=False)

        print req.text
    except requests.exceptions.ConnectionError as ce:
        print "------------------------------------------Server is unreachable.------------------------------------------"
        print ce
        print "----------------------------------------------------------------------------------------------------------"

#    req = requests.put(url, headers=headers, data=str(sensor_post), verify=False)
#    print req

    # Print out the values from sample.
    print "Temperature : " + str(temp) + " C"
    print "Pressure: " + str(pressure) + " hPa"
    print "Humidity: " + str(humidity) + "%"
    print "--------------------------------------"

    time.sleep(1)

