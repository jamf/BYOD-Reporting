# BYOD Reporting

## What were we trying to solve?

As a part of JAMF Software's BYOD program (we offer a monthly reimbursement for a staff member using a personal phone in place of a company provided phone), participants are required to have their devices managed by IT and submitting inventory to the JSS within 30 days. Reporting on "personal managed devices" (the BYOD feature of the JSS) can be tricky as:

1. personal devices cannot be members of Smart/Static Groups
2. You can perform an advanced search for "Device Ownership Type: Personal", but that includes ALL devices that have been managed as personal and would miss BYO participants who managed their phones as institutional (for access to Self Service)
3. You cannot have extension attributes on personal managed devices (this is strictly an institutional device feature).

We have a separate spreadsheet with all the serial numbers of the phones that participants have enrolled into the BYOD program. A script was written to pull the information for these devices from the JSS via the API and generate a CSV report for IT to take action on each month.

## What does it do?

This script takes a list of serial numbers in CSV format and reads in the information about the device through the JSS API. Once all of the devices in the CSV file have been read, the script will generate a CSV file that lists the name of the user assigned to the phone in the JSS, its enrolled status, the number of days since the last inventory update, and whether or not this device is still eligible for the BYOD program based on the two preceding values.

## How to use this script

This Python script can be run on Mac, Linux and Windows (Python version 2.7.6 tested).
Pass the URL to the JSS you are running against and the path to the input CSV file (this file should be a single-column CSV with only the serial numbers). Optionally you can pass the username and password that will be used to access the JSS API, but you will also be prompted for these credentials. By default, the output CSV file will be written to the same directory you are running the script from. Use the '--output' argument to specify where the file should be written.
You can also run the script with the '-h' argument to view the help text:

```
~$ python /Users/jamf-it/GitHub/BYOD-Reporting/byod-reporting.py -h
usage: BYO Reporting [-h] [-o OUTPUT_FILE] [-u USERNAME] [-p PASSWORD]
jssurl input_file

Generate a CSV file of the eligibility status of BYO devices in the JSS.

positional arguments:
jssurl               JSS URL
input_file           Path to CSV device list

optional arguments:
-h, --help           show this help message and exit
-o OUTPUT_FILE, --output OUTPUT_FILE
                     Path to write CSV (default current dir)
-u USERNAME, --username USERNAME
                     API username
-p PASSWORD, --password PASSWORD
                     API user password

Example usage:
$ ./byo-reporting.py https://my.jss.com /path/to/serial-list.csv
``` 

## License

```
Copyright (c) 2015, JAMF Software, LLC. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this
      list of conditions and the following disclaimer in the documentation and/or
      other materials provided with the distribution.
    * Neither the name of the JAMF Software, LLC nor the names of its contributors
      may be used to endorse or promote products derived from this software without
      specific prior written permission.
      
THIS SOFTWARE IS PROVIDED BY JAMF SOFTWARE, LLC "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JAMF SOFTWARE,
LLC BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
