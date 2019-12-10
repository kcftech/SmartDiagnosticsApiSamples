# Sample code for exporting indicator data and burst data from SmartDiagnostics.

from urllib import request
from urllib.request import HTTPError
from datetime import datetime
from pathlib import Path
import json
import time
import os
import argparse

# Initiates a burst data export.
#  - startMillis: Indicates the start date, represented as milliseconds from the unix epoch,
#                 within which export data will be included.
#  - endMillis: Indicates the end date, represented as milliseconds from the unix epoch,
#                 within which export data will be included.
#  - apiKey: The api key for the account that contains the data to be exported.
#  - localExportFolderPath: A path on the local file system where exported data will be placed
#                 upon export completion.
def export_account_burst_data(startMillis, endMillis, apiKey, localExportFolderPath):
    print(f'Exporting burst data between "{get_filename_friendly_date(startMillis)}" UTC and "{get_filename_friendly_date(endMillis)}" UTC')
    
    requestData = {
        "StartTime": startMillis,
        "EndTime": endMillis,
        # Specific node serial numbers for which export data will be included in the export. If this is
        # empty, the export will include all nodes for the account associated with the API key.
        "NodeSerialNumbers": [],
        # Number of chronological burst samples, starting from earliest date, to include in the export
        # within the specified time range. If set to 0, all samples in the time range are included.
        "SampleSize": 0,
        # Set to True to include the node id and the sensor type in the first two columns, respectively,
        # of the exported data set files.
        "EmbedMetadata": False
    }

    # Send the request to the web API.
    httpResponse = request.urlopen(request.Request(
        f'https://sd.kcftech.com/public/exports/burstData?apiKey={apiKey}',
        # Convert the requestData dictionary to a JSON string that is represented as an array of bytes
        # that is suitable for sending in this http request.
        data = json.dumps(requestData).encode('utf-8'),
        headers = { 'content-type': 'application/json', 'Accept': 'application/json' }
    ))
    # Read the export id from the http response.
    exportId = httpResponse.read().decode('UTF-8').strip('"')
    exportStatusResult = wait_for_export_completion(apiKey, exportId)
    # Build the full path to where the file should be output locally. The filename will include
    # the time range of the export request.
    exportFilePath = os.path.join(localExportFolderPath, f'{get_filename_friendly_date(startMillis)}--{get_filename_friendly_date(endMillis)}_burst.zip')
    handle_export_result(exportStatusResult, exportFilePath)

# Initiates an indicator data export.
#  - startMillis: Indicates the start date, represented as milliseconds from the unix epoch,
#                 within which export data will be included.
#  - endMillis: Indicates the end date, represented as milliseconds from the unix epoch,
#                 within which export data will be included.
#  - apiKey: The api key for the account that contains the data to be exported.
#  - localExportFolderPath: A path on the local file system where exported data will be placed
#           upon export completion.
def export_account_indicator_data(startMillis, endMillis, apiKey, localExportFolderPath):
    print(f'Exporting indicator data between "{get_filename_friendly_date(startMillis)}" UTC and "{get_filename_friendly_date(endMillis)}" UTC')

    requestData = {
        "StartTime": startMillis,
        "EndTime": endMillis,
        # Set to True to include the parent group hierarchy ids and names in the first two columns
        # of the exported data set files. Default value is False.
        "EmbedMetadata": False,
        # Specific indicator ids for which data will be included in the export. If this is empty (default),
        # the request will include all indicators for the account associated with the API key.
        "IndicatorIds": [],
        # Specific indicator types that should be either included or excluded from the exported data 
        # set files. If not specified, all indicator types are included. Valid types are:
        #
        #   "Voltage","DamageAccumulationAccel","Temperature","VibrationOverallCrestFactorAccel",
        #   "VibrationOverallPeakAccel","VibrationOverallRmsAccel","VibrationBandMax","VibrationOverall",
        #   "VibrationOverallPeak","VibrationOverallRms","RunningSpeed","SignalStrength","Pressure",
        #   "Flow","Humidity","Power","DifferentialPressure","GeneralizedAtoD","VibrationBandRms",
        #   "VibrationOverallSkewness","VibrationOverallKurtosis","VibrationOverallCrestFactor",
        #   "DamageAccumulation","VibrationBandRmsAccel","VibrationBandMaxAccel",
        #   "VibrationOverallSkewnessAccel", "VibrationOverallKurtosisAccel","VibrationOverallAccel",
        #   "GeneralTimeSeries","Math","OnStatistics", "OffStatistics","AlarmStatistics",
        #   "WarningStatistics","PositivePeakPressure","NegativePeakPressure", "RmsPressure",
        #   "BandPressure","OnPercentStatistics","OffPercentStatistics","AlarmPercentStatistics",
        #   "WarningPercentStatistics","DamageAccumulationPressure","OilHumidity","OilTemperature",
        #   "DamageAccumulationAccelRaw","MultiSensorDifferentialPressure","Group"
        "FilteredIndicatorTypes": [],
        # If True, the indicator types specified in the FilteredIndicatorTypes property will be excluded
        # from the exported data. If False (default), the types will be included in the exported data.
        "FilterExclude": False
    }

    # Send the request to the web API.
    httpResponse = request.urlopen(request.Request(
        f'https://sd.kcftech.com/public/exports/indicatorData?apiKey={apiKey}',
        # Convert the requestData dictionary to a JSON string that is represented as an array of bytes
        # that is suitable for sending in this http request.
        data = json.dumps(requestData).encode('utf-8'),
        headers = { 'content-type': 'application/json', 'Accept': 'application/json' }
    ))
    # Read the export id from the http response.
    exportId = httpResponse.read().decode('UTF-8').strip('"')
    exportStatusResult = wait_for_export_completion(apiKey, exportId)
    # Build the full path to where the file should be output locally. The filename will include
    # the time range of the export request.
    exportFilePath = os.path.join(localExportFolderPath, f'{get_filename_friendly_date(startMillis)}--{get_filename_friendly_date(endMillis)}_indicator.zip')
    handle_export_result(exportStatusResult, exportFilePath)

# Polls the export status API until the export has completed. Once the export has completed,
# this method returns an object describing whether the final state of the export process. Refer
# to get_export_status_result for the definition of this object.
def wait_for_export_completion(apiKey, exportId):
    exportCompleted = False
    while not exportCompleted:
        exportStatusResult = get_export_status_result(exportId, apiKey)
        exportCompleted = exportStatusResult['exportCompleted']
        if not exportCompleted:
            print('Export still in progress...')
            # Sleep for a few seconds before trying to check the status from the server again.
            time.sleep(4)
        else:
            return exportStatusResult

# Returns an object that describes the current status of a given export.
# This object structure is:
#    
#  {
#    "downloadUrl": "String",
#    "exportCompleted": Boolean,
#    "reportsProgress": Boolean,
#    "progress": Integer,
#    "error": "String"
#  }
def get_export_status_result(exportId, apiKey):
    # Send the status request to the web API.
    httpResponse = request.urlopen(request.Request(
        f'https://sd.kcftech.com/public/exports/{exportId}/status?apiKey={apiKey}',
        headers = { 'content-type': 'application/json', 'Accept': 'application/json' }
    ))
    # Read the export status JSON string from the http response.
    stringResult = httpResponse.read().decode('UTF-8')
    # Convert and return the string result as an object.
    return json.loads(stringResult)

# Downloads the exported data to the specified localExportFilePath (if the export was successful).
def handle_export_result(exportStatusResult, localExportFilePath):
    if 'downloadUrl' in exportStatusResult:
        # Download the export file to the local exportFilePath.
        request.urlretrieve(exportStatusResult['downloadUrl'], localExportFilePath)
        print(f'**Export file downloaded to {localExportFilePath}**')
    else:
        exportErrorText = exportStatusResult["error"]
        if exportErrorText == 'No data to export.':
            print(f'**The export completed with an empty data set. No file was downloaded.**')
        else:
            print(f'**Something went wrong with the export: "{exportStatusResult["error"]}"**')


def datetime_to_millis(dateTime):
    return dateTime.timestamp() * 1000

def datetime_string_to_millis(dateTimeString):
    dateTime = datetime.strptime(dateTimeString, '%Y-%m-%d %H:%M:%S')
    return datetime_to_millis(dateTime)

def millis_to_datetime(millis):
    return datetime.fromtimestamp(millis / 1000)

# Convert the input millis to a format that is allowed in a filename (something like '2019-07-20_06-12-42')
def get_filename_friendly_date(millis):
    dt = millis_to_datetime(millis)
    return dt.strftime('%Y-%m-%d %H-%M-%S')



ap = argparse.ArgumentParser()
ap.add_argument('-a', '--apikey', required = True,
   help = 'Your account API Key.')
ap.add_argument('-s', '--start', required = True,
   help = 'The start date/time of the export range in the format "YYYY-MM-DD HH:mm:ss" (e.g. "2018-09-25 00:00:00").')
ap.add_argument('-e', '--end', required = False,
   help = 'The end date/time of the export range in the format "YYYY-MM-DD HH:mm:ss" (e.g. "2018-09-25 00:00:00"). Defaults to the current date/time if omitted.')
ap.add_argument('-i', '--indicator', required = False, action='store_true',
   help = 'Specify this flag to include indicator data in the export.')
ap.add_argument('-b', '--burst', required = False, action='store_true',
   help = 'Specify this flag to include burst data in the export.')
args = vars(ap.parse_args())
if not args['burst'] and not args['indicator']:
    ap.error('You must specify at least one type of export (i.e. burst or indicator).')

apiKey = args['apikey']
startMillis = datetime_string_to_millis(args['start'])
endMillis = datetime_to_millis(datetime.utcnow())
includeIndicator = args['indicator']
includeBurst = args['burst']

if args['end'] is not None:
    endMillis = datetime_string_to_millis(args['end'])
    
# Defaults to outputting the exported files to the current path where this script is run.
localDataExportFolderPath = '.'

if includeIndicator:
    try:
       export_account_indicator_data(startMillis, endMillis, apiKey, localDataExportFolderPath)
    except HTTPError as err:
       if err.code == 401:
           print(f'**The specified API key is invalid.**')
       elif err.code == 404:
           print(f'**No indicator data exists for the specified time frame.**')
       else:
           raise
if includeBurst:
    try:
       export_account_burst_data(startMillis, endMillis, apiKey, localDataExportFolderPath)
    except HTTPError as err:
       if err.code == 401:
           print(f'**The specified API key is invalid.**')
       elif err.code == 404:
           print(f'**No burst data exists for the specified time frame.**')
       else:
           raise
    
