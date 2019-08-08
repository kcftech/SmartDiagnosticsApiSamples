# Sample code for exporting indicator data and burst data from SmartDiagnostics.

from urllib import request
from datetime import datetime
from pathlib import Path
import json
import time
import os
import zipfile

# Initiates a burst data export.
#  - startDateTimeString: Indicates the start date within which export data will be included.
#           This string is expected to be in the format 'YYYY-MM-DD HH:mm:ssT±HHMM' (see datetime_to_millis
#           method for more information).
#  - endDateTimeString: Indicates the end date within which export data will be included.
#           This string is expected to be in the format 'YYYY-MM-DD HH:mm:ssT±HHMM' (see datetime_to_millis
#           method for more information).
#  - apiKey: The api key for the account that contains the data to be exported.
#  - localExportFolderPath: A path on the local file system where exported data will be placed
#           upon export completion.
def export_burst_data(startDateTimeString, endDateTimeString, apiKey, localExportFolderPath):
    print(f'Exporting burst data between {startDateTimeString} and {endDateTimeString}.')
    
    requestData = {
        # Unix timestamp represented as milliseconds from the Unix epoch.
        "StartTime": datetime_to_millis(startDateTimeString),
        # Unix timestamp represented as milliseconds from the Unix epoch.
        "EndTime": datetime_to_millis(endDateTimeString),
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
        f'https://sdstage.kcftech.com/public/exports/burstData?apiKey={apiKey}',
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
    exportFilePath = os.path.join(localExportFolderPath, f'{get_filename_friendly_date(startDateTimeString)}--{get_filename_friendly_date(endDateTimeString)}_burst.zip')
    handle_export_result(exportStatusResult, exportFilePath)

# Initiates an indicator data export.
#  - startDateTimeString: Indicates the start date within which export data will be included.
#           This string is expected to be in the format 'YYYY-MM-DD HH:mm:ssT±HHMM' (see datetime_to_millis
#           method for more information).
#  - endDateTimeString: Indicates the end date within which export data will be included.
#           This string is expected to be in the format 'YYYY-MM-DD HH:mm:ssT±HHMM' (see datetime_to_millis
#           method for more information).
#  - apiKey: The api key for the account that contains the data to be exported.
#  - localExportFolderPath: A path on the local file system where exported data will be placed
#           upon export completion.
def export_indicator_data(startDateTimeString, endDateTimeString, apiKey, localExportFolderPath):
    print(f'Exporting indicator data between {startDateTimeString} and {endDateTimeString}.')

    requestData = {
        # Unix timestamp represented as milliseconds from the Unix epoch.
        "StartTime": datetime_to_millis(startDateTimeString),
        # Unix timestamp represented as milliseconds from the Unix epoch.
        "EndTime": datetime_to_millis(endDateTimeString),
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
        f'https://sdstage.kcftech.com/public/exports/indicatorData?apiKey={apiKey}',
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
    exportFilePath = os.path.join(localExportFolderPath, f'{get_filename_friendly_date(startDateTimeString)}--{get_filename_friendly_date(endDateTimeString)}_indicator.zip')
    handle_export_result(exportStatusResult, exportFilePath)

# Convert the input dateTime string (something like '2019-07-20 06:12:42T-0400') to
# a format that is allowed in a filename (something like '2019-07-20_06-12-42-0400')
def get_filename_friendly_date(dateTimeString):
    return f'{dateTimeString.replace(":", "-").replace(" ", "_")}'

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
        f'https://sdstage.kcftech.com/public/exports/{exportId}/status?apiKey={apiKey}',
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
        print(f'Export file downloaded to {localExportFilePath}')

        # Extract the zip file.
        with zipfile.ZipFile(localExportFilePath, 'r') as zip_ref:
            exportParentFolderPath = os.path.abspath(os.path.join(localExportFilePath, os.pardir))
            filenameWithoutExtension = Path(localExportFilePath).stem
            customOutputFolderPath = os.path.join(exportParentFolderPath, filenameWithoutExtension)
            zip_ref.extractall(customOutputFolderPath)
            print(f'Export content was extracted to {customOutputFolderPath}')
    else:
        exportErrorText = exportStatusResult["error"]
        if exportErrorText == 'No data to export.':
            print(f'The export completed with an empty data set. No file was downloaded.')
        else:
            print(f'Something went wrong with the export: "{exportStatusResult["error"]}"')

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


#
# IMPORTANT - Change this value to the API key for your account.
#
apiKey = 'YOUR_API_KEY'

# Change the start and end date to whatever time frame the included export data should occur between.
# This sample code uses a human-readable date-time format here and converts these date-time strings
# to Unix milliseconds timestamps that the export API requires.
startDateTimeString = '2019-08-07 18:00:00T-0400'
endDateTimeString = '2019-08-07 19:00:00T-0400'

# Change this to whatever output folder path the exported files should be placed.
# If this isn't changed, the files will be output to the current folder where this
# script is being run.
localExportFolderPath = '.'

# Export both the indicator data and the burst data for the specified time frame.
export_indicator_data(startDateTimeString, endDateTimeString, apiKey, localExportFolderPath)
export_burst_data(startDateTimeString, endDateTimeString, apiKey, localExportFolderPath)
