#!/usr/bin/env python

import argparse
from bash_command import *
from datetime import datetime

def timestamp():
    date = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    return date

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cycles', type=int, dest='cycles', default=1, help='number of cycles')
parser.add_argument('-l', '--log_folder', type=str, dest='log_folder', default='/tmp/', help='location of log files')
parser.add_argument('-e', '--events', nargs='+', type=int, dest='num_events', default=[-1], help='list of number of events (e.g. -e 1 10 100)')
parser.add_argument('-s', '--sites', nargs='+', type=str, dest='sites', default=['freiburg'], help='list of sites (e.g. -s freiburg local)')
parser.add_argument('-fs', '--file_sizes', nargs='+', type=str, dest='file_sizes', default=['s'], help='list of files sizes (e.g. -fs s m l)')
parser.add_argument('-d', '--debug', dest='debug', default=False, action='store_true', help='enable creation of debug files')

args = parser.parse_args()

for cycle in range(args.cycles):
    print(f"Cycle {cycle+1} of {args.cycles}\n")
    for events in args.num_events:
        for size in args.file_sizes:
            for site in args.sites:
                print(f"Now: {events} events for size {size} from site {site}")
                print('File might be already cached, delete if necessary!\n')
                if args.debug:
                    output, error = bash_command(f"./benchmark.py -l {args.log_folder} -i {timestamp()} -e {events} -fs {size} -s {site} -d")
                else:
                    output, error = bash_command(f"./benchmark.py -l {args.log_folder} -i {timestamp()} -e {events} -fs {size} -s {site}")
                print(output)
                print(error)
