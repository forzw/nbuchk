#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-12-01 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import json
import sys

# def switch json to class
class JSONObject:
     def __init__(self, d):
         self.__dict__ = d

# def switch number to boolean
def json_switch(json_data):
    dict_data=json_data['params']
    for k in dict_data.keys():
        if (dict_data[k] == 1):
            dict_data[k] = True
        elif (dict_data[k] == 0):
            dict_data[k] = False
    json_data = json.dumps(dict_data)
    return json_data

def input_json():
    # load nodejs post
    stdin_data=json.load(sys.stdin)

    # switch json to class
    json_data = json_switch(stdin_data)
    args = json.loads(json_data, object_hook=JSONObject)
    return args

