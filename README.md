# SmartDiagnosticsApiSamples

![Image description](https://www.kcftech.com/wp-content/uploads/2018/02/sd-logo.png)

Code samples and documentation for the SmartDiagnostics® API. Additional API documentation can be found at https://sd.kcftech.com/public-api/index.html

**Note that these scripts expect all dates/times to be represented in UTC (Coordinated universal time)**. In order to convert local dates/times to UTC, use the tool on this web page: https://www.timeanddate.com/worldclock/converter.html

The following example illustrates how to use this tool to convert November 10, 2019 @ 3:00pm EST (Eastern Standard Time) to the corresponding UTC date/time: ![Time zone conversion](https://github.com/KCFTech/SmartDiagnosticsApiSamples/blob/master/images/time_zone_conversion.png)

To represent the resultant UTC date/time of November 10, 2019 @ 20:00, use the following value when running the python scripts: "2019-11-10 20:00:00".

### Example Usages

##### Export group indicator data that occurred between November 19, 2019 @12am and November 21, 2019 @8:30am:

<pre><code>python export-group-data.py --apikey ACCOUNT_API_KEY --start "2019-11-19 00:00:00" --end "2019-11-21 08:30:00" --groupId GROUP_ID_TO_EXPORT --indicator</code></pre>

##### Export group indicator and group burst data that occurred between November 19, 2019 @12am and November 21, 2019 @8:30am:

<pre><code>python export-group-data.py --apikey ACCOUNT_API_KEY --start "2019-11-19 00:00:00" --end "2019-11-21 08:30:00" --groupId GROUP_ID_TO_EXPORT --indicator --burst</code></pre>

##### Export all account indicator and account burst data that occurred between November 19, 2019 @12am and November 21, 2019 @8:30am:

<pre><code>python export-account-data.py --apikey ACCOUNT_API_KEY --start "2019-11-19 00:00:00" --end "2019-11-21 08:30:00" --burst --indicator</pre></code>
