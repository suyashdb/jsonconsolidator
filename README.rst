jsonconsolidator
========================

This package finds all common k:v pairs in each task jsons to create a
corresponding json file with common k:v pairs at top level of dataset.

Once top level task jsos are created, it checks if they share any common k:v pairs to create another top level bold.json file.

 Common k:v pairs found in each case are deleted from the jsons at all other
 levels.

Install
-----

Clone this repository:

git clone https://github.com/suyashdb/jsonconsolidator.git

cd jsonconsolidator

python setup.py install

Usage
-----
[Default]

jsonconsolidator path/to/bids/dataset

   This will just give list of files that will be changed/deleted or created new.

Options:

jsonconsolidator path/to/bids/dataset -v

   This will just give list of files that will be changed/deleted or created new.


jsonconsolidator path/to/bids/dataset final

   Once you are happy with the consolidation and output by '-v' option, this will
   actually change files and create new files. Back up of old files will be stored
   under bids_dataset_path/.backup_json.
