jsonconsolidator
========================

This package finds all common k:v pairs in each task jsons to create a
corresponding json file with common k:v pairs at top level of dataset.

Once top level task jsos are created, it checks if they share any common k:v pairs to create another top level bold.json file.

 Common k:v pairs found in each case are deleted from the jsons at all other
 levels.

Installation:
------------

Clone this repository:

`git clone https://github.com/suyashdb/jsonconsolidator.git`

`cd jsonconsolidator`

`python setup.py install`

Usage:
-----
[Default]

`jsonconsolidator path/to/bids/dataset`

   Default mode is verbose. This gives list of files that will be changed/deleted or created new

Options:

i).
   `jsonconsolidator path/to/bids/dataset -v`

      verbose mode `-v` gives list of files that will be changed/deleted or added new


ii).
   `jsonconsolidator path/to/bids/dataset final`

      Once changes suggested in verbose mode are reviewed and correct, `final` option changes files and create back up for old files.
      Old files are stored under `path_to_bids_dataset/sourcedata/backup_json`
