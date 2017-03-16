jsonconsolidator
========================

This package finds all common k:v pairs in each task jsons to create a
corresponding json file with common k:v pairs at top level of dataset.

 Once top level task jsos are created, it checks if they share any common k:v
 pairs to create another top level bold.json file.

 Common k:v pairs found in each case are deleted from the jsons at all other
 levels.

Install
-----

Clone this repository by
git clone https://github.com/suyashdb/jsonconsolidator.git
cd jsonconsolidator
python setup.py install

Usage
-----
jsonconsolidator path/to/bids/dataset
