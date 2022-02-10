#!/usr/bin/env python

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, dest='input', default='benchmarks.csv', help='location of the csv file')
parser.add_argument('-o', '--output_path', type=str, dest='output_path', default='/tmp/', help='path to store the figures')

args = parser.parse_args()

df = pd.read_csv(args.input)

#plot all results, split by file size

fig, axes = plt.subplots(1, 3, figsize=(22,7), sharey=True)

sns.barplot(ax=axes[0],
            x='n_events',
            y='time',
            hue='site',
            data=df[(df.filesize == 's')],
            ci='sd',
            capsize=0.1,
            errwidth=1.)

sns.barplot(ax=axes[1],
            x='n_events',
            y='time',
            hue='site',
            data=df[(df.filesize == 'm')],
            ci='sd',
            capsize=0.1,
            errwidth=1.)

sns.barplot(ax=axes[2],
            x='n_events',
            y='time',
            hue='site',
            data=df[(df.filesize == 'l')],
            ci='sd',
            capsize=0.1,
            errwidth=1.)

plt.subplots_adjust(wspace=0.)

axes[0].set_yscale('log')
axes[0].set_ylim([1,100000])

axes[0].tick_params(labelsize='x-large')
axes[1].tick_params(labelsize='x-large')
axes[2].tick_params(labelsize='x-large')

axes[0].grid(True, which='both')
axes[1].grid(True, which='both')
axes[2].grid(True, which='both')

axes[0].legend(title=None, loc='upper left', fontsize='x-large')
axes[1].get_legend().remove()
axes[2].get_legend().remove()

axes[0].set_title('Small file (1.3 GB)', fontsize='x-large')
axes[1].set_title('Medium file (4.9 GB)', fontsize='x-large')
axes[2].set_title('Large file (13 GB)', fontsize='x-large')

axes[0].set_ylabel('Time [s]', fontsize='x-large')
axes[1].set_ylabel('')
axes[2].set_ylabel('')

axes[0].set_xlabel('No. of events', fontsize='x-large')
axes[1].set_xlabel('No. of events', fontsize='x-large')
axes[2].set_xlabel('No. of events', fontsize='x-large')

fig.savefig(args.output_path+'all_results.pdf')

#plot results for freiburg and local, results for different file sizes are merged

fig, ax = plt.subplots()

sns.barplot(ax=ax,
            x='n_events',
            y='time',
            hue='site',
            data=df[(df.site.isin(['freiburg','local']))],
            ci='sd',
            capsize=0.1,
            errwidth=1.)

ax.set_yscale('log')
fig.savefig(args.output_path+'freiburg_vs_local_sizes_merged.pdf')
