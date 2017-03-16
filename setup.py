# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


# version = re.search(
#     '^__version__\s*=\s*"(.*)"',
#     open('jsonconsolidator.jsonconsolidator.py').read(),
#     re.M
#     ).group(1)



setup(
    name = "BIDS json-consolidator",
    packages = ["jsonconsolidator"],
    entry_points = {
        "console_scripts": ['jsonconsolidator = jsonconsolidator.jsonconsolidator:main']
        },
    version = '0.1.0',
    description = "Python command line application for bids json consolidator .",
    long_description = "This package finds common k:v pairs in all jsons in bids dataset and creates json files at top level.",
    author = "Suyash Bhogawar",
    author_email = "abc@gmail.com",
    )
