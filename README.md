# SmartDiagnosticsApiSamples

![Image description](https://www.kcftech.com/wp-content/uploads/2018/02/sd-logo.png)

Code samples and documentation for the SmartDiagnostics® API. Additional API documentation can be found at https://sd.kcftech.com/public-api/index.html

**Initial Setup (Windows):**

1) Download and install Python 3, and make sure to check the box "Add Python 3.8 to PATH" on the installation screen: https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe

![Install Python](https://github.com/KCFTech/SmartDiagnosticsApiSamples/blob/master/images/install_python.png)

2) Download and install 7zip: https://www.7-zip.org/a/7z1900-x64.exe

3) Download the SmartDiagnostics python code from this repository, and extract this file using 7zip: https://github.com/KCFTech/SmartDiagnosticsApiSamples/archive/master.zip

![Extract code](https://github.com/KCFTech/SmartDiagnosticsApiSamples/blob/master/images/extract_code.png)

<br/><br/>
**Run The Code**

1) Open a Windows command prompt. Click on the Windows menu, enter the text "Command Prompt", and click the corresponding icon.

2) In the prompt, change to the directory where you extracted the SmartDiagnostics python code to in the "Initial Setup" section. To do this, use the **cd** command. For example:

<pre><code>cd C:\Users\myusername\Downloads\SmartDiagnosticsApiSamples-master</pre></code>

3) Run the desired export command (refer to the Example Usages section below for details on how to run the exports).

---
<br/><br/>

### Example Usages

##### Export group indicator data that occurred between November 19, 2019 @12am and November 21, 2019 @8:30am:

<pre><code>python export-group-data.py --apikey ACCOUNT_API_KEY --start "2019-11-19 00:00:00" --end "2019-11-21 08:30:00" --groupId GROUP_ID_TO_EXPORT --indicator</code></pre>

##### Export group indicator and group burst data that occurred between November 19, 2019 @12am and November 21, 2019 @8:30am:

<pre><code>python export-group-data.py --apikey ACCOUNT_API_KEY --start "2019-11-19 00:00:00" --end "2019-11-21 08:30:00" --groupId GROUP_ID_TO_EXPORT --indicator --burst</code></pre>

##### Export all account indicator and account burst data that occurred between November 19, 2019 @12am and November 21, 2019 @8:30am:

<pre><code>python export-account-data.py --apikey ACCOUNT_API_KEY --start "2019-11-19 00:00:00" --end "2019-11-21 08:30:00" --burst --indicator</pre></code>

**Important Note: the above scripts expect all dates/times to be represented in UTC (Coordinated universal time)**. In order to convert local dates/times to UTC, use the tool on this web page: https://www.timeanddate.com/worldclock/converter.html

The following example illustrates how to use this tool to convert November 10, 2019 @ 3:00pm EST (Eastern Standard Time) to the corresponding UTC date/time: ![Time zone conversion](https://github.com/KCFTech/SmartDiagnosticsApiSamples/blob/master/images/time_zone_conversion.png)

To represent the resultant UTC date/time of November 10, 2019 @ 20:00, use the following value when running the python scripts: "2019-11-10 20:00:00".
