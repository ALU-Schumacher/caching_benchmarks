# caching_benchmarks

This is a collection of scripts for benchmarking caching setups and visualization of the results.\
Nothing concerning the caching setup is done with these scripts: it is the responsibility of the user to (de-)activate any caching functionality and to control/check the presence of files in the cache space.

## Files

To provide a varity of different file sizes and event numbers, three files are used: small (1.3 GB, 50k events), medium (5.2 GB, 200k events), and large (13 GB, 500k events). The files contain simulated ttbar events.
Members of the ATLAS collaboration can get the files from `UNI-FREIBURG_LOCALGROUPDISK`:

```
root://sedoor1.bfg.uni-freiburg.de:1094//pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/dsammel/fb/5a/small.root
root://sedoor1.bfg.uni-freiburg.de:1094//pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/dsammel/52/b5/medium.root
root://sedoor1.bfg.uni-freiburg.de:1094//pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/dsammel/04/71/large.root
```

An example setup to download the files is:

```
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
lsetup rucio
voms-proxy-init -voms atlas
rucio download user.dsammel:small.root user.dsammel:medium.root user.dsammel:large.root --rse UNI-FREIBURG_LOCALGROUPDISK
```

### File creation

Otherwise, the files can be created with `pythia8.C`:

Follow the instructions on http://home.thep.lu.se/~torbjorn/Pythia.html and http://home.thep.lu.se/~torbjorn/pythia83html/ROOTusage.html (Standalone usage) to install `PYTHIA8`, e.g. in the folder pythia8. An installation of `ROOT` is required.

Compile `main92.cc` in `pythia8/examples`

To simulate events with the CLI, start `ROOT` and execute the following commands:

```
gSystem->Load("pythia8/lib/libpythia8.so")
gSystem->Load("pythia8/examples/main92.so")
.x pythia8.C(50000)
```

This will simulate 50k events and store the output in `pytree.root`.


## Benchmarks

`ROOT` and `python3` are required for running the benchmarks.
An example setup for members of the ATLAS collaboration is:

```
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
lsetup "root 6.22.06-x86_64-centos7-gcc8-opt"
```

### benchmark.py

The benchmarks are steered with `benchmark.py`.

```
usage: benchmark.py [-h] [-l LOG_FOLDER] [-i IDENTIFIER] [-e NUM_EVENTS]
                    [-s SITE] [-fs FILE_SIZE] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_FOLDER, --log_folder LOG_FOLDER
                        location of log files
  -i IDENTIFIER, --identifier IDENTIFIER
                        identifier for the log files
  -e NUM_EVENTS, --events NUM_EVENTS
                        number of events
  -s SITE, --site SITE  site (freiburg, kit, triumf, local, ...)
  -fs FILE_SIZE, --file_size FILE_SIZE
                        size of the file (s, m, l)
  -d, --debug           enable creation of debug files
```

Site example:

```
[freiburg]
site_url = root://sedoor1.bfg.uni-freiburg.de:1094/
site_folder = /pnfs/bfg.uni-freiburg.de/data/atlaslocalgroupdisk/rucio/user/dsammel/
```

File example:

```
[s]
file_name = small.root
sub_folder = fb/5a/
max_events = 50000
```

Additional sites and files can be added by following this format.
The sites `triumf` and `kit` are just examples and will probably not work, since the replicas of the files have a lifetime and will eventually be deleted. `freiburg` should work, since there the files have infinite lifetime.\
If the files are replicated to any other site, the fields `site_url` and `site_folder` in `sites.ini`, and the field `sub_folder` in `files.ini` have to be adjusted.
There's also the `local` option in `sites.ini`:

```
[local]
site_url = 
site_folder = /path/to/folder/with/files/
```

This can be used to access local copies of the files. `site_url` has to remain empty and `site_folder` has to be adjusted accordingly.

`benchmark.py` calls `event_loop.py` (see next section). The time for the completion of `event_loop.py` and information about the used options are then stored in a `.json` file.

### event_loop.py

The actual work is done in `event_loop.py`

```
usage: event_loop.py [-h] [-f FILE_NAME] [-e NUM_EVENTS]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file FILE_NAME
                        path to file
  -e NUM_EVENTS, --events NUM_EVENTS
                        number of events
```

Several operations that happen in typical analyses are performed:\
The file is opened with [PyROOT](https://root.cern/manual/python/) and a loop over the number of events is performed. In the loop, the number of particles is retrieved for each event. Another loop is performed over the number of particles. For each particle, the pseudorapidity is retrieved and filled in a histogram. In addition, a four-vector is constructed of all outgoing particles. The mass of this four-vector, which represents the ttbar system, is retrieved and stored in a histogram.

### benchmark_loop.py

The output of `benchmark.py` is just 1 result for 1 site, 1 file, and 1 number of events. To collect statistics for different combinations of options, `benchmark_loop.py` can be used.

```
usage: benchmark_loop.py [-h] [-c CYCLES] [-l LOG_FOLDER] [-e NUM_EVENTS [NUM_EVENTS ...]] [-s SITES [SITES ...]] [-fs FILE_SIZES [FILE_SIZES ...]] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -c CYCLES, --cycles CYCLES
                        number of cycles
  -l LOG_FOLDER, --log_folder LOG_FOLDER
                        location of log files
  -e NUM_EVENTS [NUM_EVENTS ...], --events NUM_EVENTS [NUM_EVENTS ...]
                        list of number of events (e.g. -e 1 10 100)
  -s SITES [SITES ...], --sites SITES [SITES ...]
                        list of sites (e.g. -s freiburg local)
  -fs FILE_SIZES [FILE_SIZES ...], --file_sizes FILE_SIZES [FILE_SIZES ...]
                        list of files sizes (e.g. -fs s m l)
  -d, --debug           enable creation of debug files
```

The script performs nested loops over the number of events, files sizes, and sites, and calls `benchmark.py` with the respective arguments. As identifier, a simple timestamp is used.

## Plotting

Python can be used to visualize the results. The necessary packages for the example provided in this repository can be installed in a virtual environment with `pip`. To avoid potential conflicts, this should be done in a new session, i.e. without the ROOT setup from the benchmarking step.

Creation of the virtual environment:

```
python3 -m venv virtual_environment
```

Activation of the virtual environment:

```
source virtual_environment/bin/activate
```

Installation of the packages:

```
pip install -r requirements.txt
```

Only the "Activation" step has to be done in later sessions.

### aggregate_logs.py

The first step is the aggregation of all created logfiles with `aggregate_logs.py` using [Pandas](https://pandas.pydata.org/).

```
usage: aggregate_logs.py [-h] [-l LOG_FOLDER] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_FOLDER, --log_folder LOG_FOLDER
                        location of log files
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        name of output file
```

The script creates a dataframe using all `.json` files that are present in the path specified with `-l`. The dataframe is stored in the `csv` format, but Pandas offers many other options.

### plotting.py

Finally, `plotting.py` uses the information in the dataframe to create plots using [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/).

```
usage: plotting.py [-h] [-i INPUT] [-o OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        location of the csv file
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        path to store the figures
```

The script contains two examples: one plot with all the results separated by site, file size, and number of events, and one plot where only two sites are compared and where the files sizes have been merged.

## Full example test run

If the environment is set up, including a local copy of the files and the modified entry in `sites.ini`, an example test run would be:

```
python benchmark_loop.py -c 3 -e 1 100 1000 -s freiburg local -fs s m l
```

The `-s freiburg` option only works for members of the ATLAS collaboration.

```
python aggregate_logs.py
```
```
python plotting.py
```

This will create log files and plots in `/tmp/`.