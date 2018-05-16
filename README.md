# check_storix
Nagios Plugin to check Storix Logfiles for Errors

usage: check_storix.py [-h] [-f LOGFILEPATH] [-d DAYSTOCHECK]

Checks Storix Logs

optional arguments:
  -h, --help            show this help message and exit
  -f LOGFILEPATH, --file LOGFILEPATH
                        the storix logfile that should be checked
  -d DAYSTOCHECK, --days DAYSTOCHECK
                        how many days back should be checked for errors in the
                        logfile
