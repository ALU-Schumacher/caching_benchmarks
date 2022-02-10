#!/usr/bin/env python

import timeit
import argparse
import configparser
import json
import sys
from bash_command import *
from shutil import which

config = configparser.ConfigParser()
config.read(['sites.ini','files.ini'])

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log_folder', type=str, dest='log_folder', default='/tmp/', help='location of log files')
parser.add_argument('-i', '--identifier', type=str, dest='identifier', default='benchmark', help='identifier for the log files')
parser.add_argument('-e', '--events', type=int, dest='num_events', default=-1, help='number of events')
parser.add_argument('-s', '--site', type=str, dest='site', default='freiburg', help='site (freiburg, kit, triumf, local, ...)')
parser.add_argument('-fs', '--file_size', type=str, dest='file_size', default='s', help='size of the file (s, m, l)')
parser.add_argument('-d', '--debug', dest='debug', default=False, action='store_true', help='enable creation of debug files')

args = parser.parse_args()

if which('root') is None:
   sys.exit('ROOT installation not found!\nAborting')

try:
   config[args.site]
except:
   sys.exit(f"Site '{args.site}' not found in sites.ini!\nAborting")

try:
   config[args.file_size]
except:
   sys.exit(f"File size '{args.file_size}' not found in files.ini!\nAborting")

site_url = config[args.site]['site_url']
site_folder = config[args.site]['site_folder']

file_name = config[args.file_size]['file_name']
if args.site == 'local':
   sub_folder = ''
else:
   sub_folder = config[args.file_size]['sub_folder']
max_events = int(config[args.file_size]['max_events'])

file_path = site_url + site_folder + sub_folder + file_name

if args.num_events > max_events:
   sys.exit(f"Maximum number of events for file size {args.file_size} is {max_events}, you requested {args.num_events}!\nAborting")
elif args.num_events == -1:
   num_events = max_events
else:
   num_events = args.num_events

info_dict = {}
info_dict['filesize'] = args.file_size
info_dict['site'] = args.site
info_dict['n_events'] = num_events

print('================================================================')
print(f"Setup complete:\n\nSite: {args.site}\nFile size: {args.file_size}\nNo. of events: {num_events}\n\nStarting event loop!\n")

tic = timeit.default_timer()

output, error = bash_command(f"./event_loop.py -f {file_path} -e {num_events}")
   
toc = timeit.default_timer()

print('Event loop finished, writing output files!\n')

time = toc-tic

info_dict['time'] = time

if args.debug:   
   with open(f"{args.log_folder}/{args.identifier}_{args.site}_{args.file_size}_{num_events}_output.txt",'w') as out_file:
      out_file.write(output)

   with open(f"{args.log_folder}/{args.identifier}_{args.site}_{args.file_size}_{num_events}_error.txt",'w') as error_file:
      error_file.write(error)

with open(f"{args.log_folder}/{args.identifier}_{args.site}_{args.file_size}_{num_events}.json", 'w') as json_file:
   json.dump(info_dict, json_file, indent=4, sort_keys=True)

print('Done!')
print('================================================================\n')
