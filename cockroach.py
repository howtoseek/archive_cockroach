#!/usr/bin/python3

import requests
import argparse
from datetime import datetime, timedelta

def makeRequestToArchive(apiUrl, requestParam):
    try:
        response = requests.get(apiUrl, params=requestParam)
    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')
    except requests.exceptions.ReadTimeout:
        print('Oops. Read timeout occured')
    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')

    return response.text

def importRobots():
    urlParam = combineUrlParam()
    urlParam['url'] = "{}{}".format(urlParam['url'], '/robots.txt')
    response = makeRequestToArchive(URL_API_CDX, urlParam)

    return response

def checkRangeOfDate():
    urlParam = combineUrlParam()
    makeRequestToArchive()

'''Prepare URL params for 'get' request to API'''
def prepareGetRequestParams(action):
    recivedCmdParam = vars(parseCmdParam())
    urlParams = {'url': '',
                 ''}



    #return  urlParams

'''Render help menu and parse cmd params'''
def parseCmdParam():
    defaultStartDate = datetime.strftime((datetime.now() - timedelta(days=365)), "%Y%m%d")
    defaultEndDate = datetime.strftime(datetime.now(), "%Y%m%d")

    parser = argparse.ArgumentParser(description='See avalible options',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    actionSubparser = parser.add_subparsers(description='Action commands:',
                                            help='Type \'%(prog)s action_command -h\' to view additional options.')
    robotsParser = actionSubparser.add_parser('robots', help='Get all robots.txt records for a domain')
    robotsParser.set_defaults(action='robots')
    robotsParser.add_argument('-d', '--domain',
                        action='store',
                        metavar='example.com',
                        required=True,
                        help='Domain for which to search')
    dateRangeGroup = robotsParser.add_argument_group('Historical data range(use as a pair, only together)')
    dateRangeGroup.add_argument('-s', '--startdate',
                        action='store',
                        default=defaultStartDate,
                        metavar='yyyymmdd',
                        help='Start date in yyyymmdd format. For example 19700130')
    dateRangeGroup.add_argument('-e', '--enddate',
                        action='store',
                        default=defaultEndDate,
                        metavar='yyyymmdd',
                        help='End date in yyyymmdd format. For example 19700130')
    rangeParser = actionSubparser.add_parser('range', help='Check available date range in history')
    rangeParser.set_defaults(action='range')
    rangeParser.add_argument('-d', '--domain',
                        action='store',
                        metavar='example.com',
                        required=True,
                        help='Domain for which to search')

    return parser.parse_args()

URL_API_CDX = 'http://web.archive.org/cdx/search/cdx?'
doAction = parseCmdParam().action

if doAction == 'robots':
    prepareGetParams()
elif doAction == 'range':
    print('Rangers')
    print(parseCmdParam())





















