# Sample code for importing general time series data into SmartDiagnostics.

from urllib import request
from urllib.error import HTTPError
from datetime import datetime
import json
import time
import sys

# Convenience method to convert a date-time string to a unix timestamp in milliseconds.
# Accepts a date-time string of the format 'YYYY-MM-DD HH:mm:ssT±HHMM, where
#	
#    YYYY = the 4-digit year
#    MM = the 2-digit month
#    DD = the 2-digit day of the month
#    HH = the 2-digit hour of the day
#    mm = the 2-digit minute of the hour
#    ss = the 2-digit seconds in the minute
#    ±HHMM = the timezone offset from UTC (e.g. -0400, +1030, +0000)
def datetime_to_millis(dateTimeString):
    dateTime = datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%ST%z')
    return (int)(dateTime.timestamp() * 1000)

requestData = {
    "Nodes": [{
        # Arbitrary node id. In the context of general time series data, a node is a
        # logical grouping of data sources, and this can represent a Pi system, for example.
        "UniqueId": "Pi System",
        "Sensors": [{
            # Arbitrary value that identifies a data source (e.g. a Pi item).
            "SensorRole": "my.item.id",
            # Array of time series data. Each data point consists of a unix timestamp
            # and an associated floating-point value.
            "DataPoints": [{
                "Time": datetime_to_millis('2019-08-01 06:31:12T-0400'),
                "Value": 3.61
            }, {
                "Time": datetime_to_millis('2019-08-01 06:33:45T-0400'),
                "Value": 3.57
            }]
        }]
    }]
}

#
# IMPORTANT - Change this value to the API key for your account.
#
apiKey = 'YOUR_API_KEY'

# Send the request to the web API.
try:
    httpResponse = request.urlopen(request.Request(
        f'https://sd.kcftech.com/public/imports?apiKey={apiKey}',
        # Convert the requestData dictionary to a JSON string that is represented as an array of bytes
        # that is suitable for sending in this http request.
        data = json.dumps(requestData).encode('utf-8'),
        headers = { 'content-type': 'application/json', 'Accept': 'application/json' }
    ))
    print(f'API POST success.')
except HTTPError as e:
    print(f'API POST failure: {e}')
