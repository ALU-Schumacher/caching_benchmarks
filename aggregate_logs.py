#!/usr/bin/env python

import argparse
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log_folder', type=str, dest='log_folder', default='/tmp/', help='location of log files')
parser.add_argument('-o', '--output_file', type=str, dest='output_file', default='benchmarks.csv', help='name of output file ')

args = parser.parse_args()

logs = Path(args.log_folder).glob('*.json')

df_list = [pd.DataFrame([pd.read_json(log, typ='series')]) for log in logs]
df = pd.concat(df_list, ignore_index=True)

df.to_csv(args.output_file)

