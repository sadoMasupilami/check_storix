#!/usr/bin/python

###########################################################
# written by Klug Michael for KNAPP (michiklug85(at)gmail.com)
###########################################################

import re
import argparse
import datetime

# Parsing arguments
parser = argparse.ArgumentParser(description='Checks Storix Logs')
parser.add_argument('-f', '--file', action='store', default='/storix/logs/trace.log', dest='logFilePath',
                    help='the storix logfile that should be checked')
parser.add_argument('-d', '--days', action='store', default=10, dest='daysToCheck',
                    help='how many days back should be checked for errors in the logfile')

args = parser.parse_args()

logFilePath = args.logFilePath
# logFilePath = 'trace_wehkamp.log'
daysToCheck = int(args.daysToCheck)

storixRegex = "SBA (?P<status>[a-zA-Z]+):[\s\S]*?(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (?P<month>...) (?P<day>\d\d) (?P<hour>\d\d):(?P<min>\d\d):(?P<sek>\d\d)(?: AM| PM)? \w{2,4} (?P<year>\d{4})\n(?P<text>.*)"


def get_storix_list():
    try:
        with open(logFilePath, "r") as f:
            fileToParse = f.read()
    except:
        print "File could not be oppened"
        exit(2)

    storixPattern = re.compile(storixRegex)
    storixMatcher = storixPattern.findall(fileToParse)
    return storixMatcher


def convertMonth(monthString):
    if monthString == 'Jan':
        return 1
    elif monthString == 'Feb':
        return 2
    elif monthString == 'Mar':
        return 3
    elif monthString == 'Apr':
        return 4
    elif monthString == 'May':
        return 5
    elif monthString == 'Jun':
        return 6
    elif monthString == 'Jul':
        return 7
    elif monthString == 'Aug':
        return 8
    elif monthString == 'Sep':
        return 9
    elif monthString == 'Oct':
        return 10
    elif monthString == 'Nov':
        return 11
    elif monthString == 'Dec':
        return 12


def findLastXDaysLogEntries(days, storixParsedLog):
    returnList = []
    delta = datetime.timedelta(days=days)
    now = datetime.datetime.now()
    dateToCompare = now - delta
    # print dateToCompare
    for match in storixParsedLog:
        # print match[0]
        if match[0] > dateToCompare:
            returnList.append(match)
    return returnList


def printAllEntries(storixParsedLog):
    for entry in storixParsedLog:
        print str(entry[0]) + " Status: " + entry[1] + " Message: " + entry[2]


def transformMatches(storixParsedLog):
    returnList = []
    for match in storixParsedLog:
        tempDate = datetime.datetime(int(match[6]), convertMonth(match[1]), int(match[2]), int(match[3]),
                                     int(match[4]), int(match[5]))
        # returnList.append((tempDate, match[0], match[7]))
        returnList.insert(0, (tempDate, match[0], match[7]))
    return returnList


def doAnalysis(relevantEntries):
    if len(relevantEntries) <= 0:
        print "CRITICAL no entries found in the checked timeframe"
        exit(2)
    for entry in relevantEntries:
        if entry[1] == "ERROR" or entry[1] == "JOBERR" or entry[1] == "VOLCHG":
            print "CRITICAL - " + str(entry[0]) + " Status: " + entry[1] + " Message: " + entry[2]
            exit(2)
    print "OK - no errors found"
    exit(0)


storixParsedLog = get_storix_list()
storixEntries = transformMatches(storixParsedLog)
relevantEntries = findLastXDaysLogEntries(daysToCheck, storixEntries)
# printAllEntries(relevantEntries)
doAnalysis(relevantEntries)
print "UNKNOWN"
exit(3)
