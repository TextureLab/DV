#!/usr/bin/env python

""" dataIO.py : Data input and output manager classes."""

__author__ = "Pierre Le Bras, Heriot Watt University"
__license__ = "Creative Commons Attribution 4.0 International License"
__version__ = "1.0"

import json
from functools import reduce


class DataReader:

    def __init__(self, data_file_name=""):
        self.data_file_name = data_file_name

    def set_data_file_name(self, string):
        self.data_file_name = string

    def read_file(self):
        print('reading file')
        return json.loads(open(self.data_file_name).read())

    def get_texts(self, path=None, id_accessor="id", text_accessors=None):
        if text_accessors is None:
            text_accessors = ["text"]
        if path is None:
            path = []
        j = self.read_file()
        print('getting texts')
        for a in path:
            j = j[a]
        return {item[id_accessor]: reduce(lambda x, y: item[x] + " " + item[y], text_accessors) for item in j}


class DataWriter:

    def __init__(self, file_name=""):
        self.file_name = file_name

    def set_data_file_name(self, string):
        self.file_name = string

    def write(self, data):
        open(self.file_name, 'w').write(json.dumps(data))
