#!/usr/bin/env python3.5

import requests
import argparse
from datetime import datetime, timedelta
import json
import asyncio
import aiohttp
import async_timeout


def makeRequestToArchive(urlApi, requestParams):
    try:
        response = requests.get(urlApi, params=requestParams)
        return response.text
    except requests.exceptions.ConnectTimeout:
        print('Something went wrong:\nConnection timeout occured!')
    except requests.exceptions.ReadTimeout:
        print('Something went wrong:\nRead timeout occured')
    except requests.exceptions.ConnectionError:
        print('Something went wrong:\n'
              'Seems like dns lookup failed. Try ping {}'.format(requestParams['url']))


def checkAvalibleDateRange(requestParams):
    checkAval = json.loads(
        makeRequestToArchive(URL_API_AVL, {'url': requestParams['url']})
    )
    if checkAval['archived_snapshots'] == {}:
        return None

    requestParams['limit'] = '1'
    earliestDate = json.loads(
        makeRequestToArchive(URL_API_CDX, requestParams)
    )[1][0]
    requestParams['limit'] = '-1'
    latestDate = json.loads(
        makeRequestToArchive(URL_API_CDX, requestParams)
    )[1][0]

    return [earliestDate, latestDate]


def prepareGetRequestParams():
    recivedCmdOptions = parseCmdOptions()
    urlParams = {}

    if recivedCmdOptions['action'] == 'robots':
        urlParams['action'] = recivedCmdOptions['action']
        urlParams['url'] = recivedCmdOptions['domain'] + '/robots.txt'
        urlParams['from'] = recivedCmdOptions['startdate']
        urlParams['to'] = recivedCmdOptions['enddate']
        urlParams['fl'] = 'timestamp'
        urlParams['filter'] = 'statuscode:200'
        urlParams['output'] = 'json'
    elif recivedCmdOptions['action'] == 'range':
        urlParams['action'] = recivedCmdOptions['action']
        urlParams['url'] = recivedCmdOptions['domain']
        urlParams['fl'] = 'timestamp'
        urlParams['filter'] = 'statuscode:200'
        urlParams['output'] = 'json'

    # return list of params
    return urlParams


def splitUrlList(urlList, chunkSize):
    splitedList = [urlList[i:i + chunkSize] for i in range(0, len(urlList), chunkSize)]

    return splitedList

# Render help menu and parse cmd params
def parseCmdOptions():
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
    dateRangeGroup = robotsParser.add_argument_group('Historical data range(Default range: all last year)')
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

    args = vars(parser.parse_args())

    if args.get('action') == None:
        parser.print_help()
        exit(1)
    else:
        return  args


async def fetch(url, session):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def mainCycle(loop, urlList):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for i in splitUrlList(urlList, DOWNLOAD_THREAD_NUMBER):
            for url in i:
                task = asyncio.ensure_future(fetch(url, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks, loop=loop)

            percentComplite = len(responses) * 100 // len(urlList)
            barLine = '#' * percentComplite + '.' * (100 - percentComplite)
            print('Complite: [{}] {} %\r'.format(barLine, percentComplite), end='')

        return responses


# Wayback CDX Server API
URL_API_CDX = 'http://web.archive.org/cdx/search/cdx?'
# Wayback Availability JSON API
URL_API_AVL = 'https://archive.org/wayback/available?'
# Five thread work fine, Additional threads blocked by API server and the download ends with an exception
DOWNLOAD_THREAD_NUMBER = 5

urlParams = prepareGetRequestParams()

if __name__ == '__main__':
    if urlParams['action'] == 'robots':
        listAvalArchiveData = json.loads(
            makeRequestToArchive(URL_API_CDX, urlParams)
        )

        if listAvalArchiveData == []:
            print('No data was found for this domain. Verify that the domain name or date range is entered correctly.')
            exit(1)
        listAvalArchiveData.pop(0)

        urlToFetchPattern = 'https://web.archive.org/web/{0}/{1}'
        urlToFetchList = [urlToFetchPattern.format(x[0], urlParams['url']) for x in listAvalArchiveData]

        loop = asyncio.get_event_loop()
        recivedData = loop.run_until_complete(mainCycle(loop, urlToFetchList))

        # remove duplicates
        resultRobotsRecords = []
        robotsRecordsUniqueSelect = set()
        for line in recivedData:
            for record in line.split('\n'):
                if record in robotsRecordsUniqueSelect:
                    continue
                robotsRecordsUniqueSelect.add(record)
                resultRobotsRecords.append(record)

        # print records
        print('\nFound {0} unique robotx.txt records for the period from {1} to {2}\n{3}'.format(
            len(resultRobotsRecords),
            urlParams['from'],
            urlParams['to'],
            '-' * 100))
        for record in resultRobotsRecords:
            print(record)

    elif urlParams['action'] == 'range':
        response = checkAvalibleDateRange(urlParams)
        if response != None:
            print("For the domain {0} available data for the period:\n".format(urlParams['url']) +
                  "Earliest date: " + response[0] + "\n" +
                  "Latest date: " + response[1])
        else:
            print("There is no data in the web.archive.org for the domain {}".format(urlParams['url']))
