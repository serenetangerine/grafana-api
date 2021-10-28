#!/usr/bin/env python3

import argparse
import json
import os
import requests


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', '-t', help='Grafana API token', type=str, required=True)
    parser.add_argument('--server', '-s', help='Grafana server url', type=str, required=True)
    parser.add_argument('--directory', '-d', help='Directory to export dashboard json files', type=str, default='./dashbord-export/')
    
    args = parser.parse_args()
    return args


def createDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def parseFilename(title):
    title = title.replace(' ', '-')
    title = title.replace('/', '_')
    title = title.replace(':', '')
    return title


def main():
    args = getArguments()

    server = args.server
    token = args.token
    directory = args.directory
    header = {'Authorization': 'Bearer %s' % (token)}

    print('Creating directory %s...' % (directory))
    createDirectory(directory)

    print('Fetching dashboards...')
    response = requests.get('%s/api/search?query=&' % (server), headers=header)
    response.raise_for_status()
    dashboards = response.json()

    print('\n')
    for dashboard in dashboards:
        print('Exporting: %s' % (dashboard['title']))
        response = requests.get('%s/api/dashboards/uid/%s' % (server, dashboard['uid']), headers=header)
        data = response.json()['dashboard']
        data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

        title = parseFilename(data[0]['title'])

        with open('%s%s.json' % (directory, title), 'w') as file:
            file.write(data)
            file.write('\n')

        print('Created %s%s.json' % (directory, title))




if __name__ == '__main__':
    main()
