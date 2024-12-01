#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-10-24 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import re
import csv
import subprocess as sb
from nbu.check_env import *

def read_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    try:
      return lines[3:]
    except ValueError:
      return []

def get_pool_number(src_data):
    ret_json = {}
    key_pool = ''
    for line in src_data:
        if not (line and line[:-1]):
            continue
        line = line[:-1]
        if line.endswith('pool'):
            key_pool = line
            if key_pool not in ret_json:
                ret_json[key_pool] = {"AVAILABLE":0,"FULL":0,"FROZEN":0}
            continue
        else:
            pool_type = line.split()[-1]
            if pool_type == "ACTIVE":
                ret_json[key_pool]["AVAILABLE"] += 1
            else:
                ret_json[key_pool][pool_type] += 1
    return ret_json

def check_tape_used(args):

    logger.info('runcmd: start get tape used')

    file_lines = read_file(args.tape_list)
    ret_json = get_pool_number(file_lines)
    out_csv = []
    for key,type_values in ret_json.items():
        item = [args.master]
        item.append(key)
        total = type_values["AVAILABLE"] + type_values["FULL"] + type_values["FROZEN"]
        item.append(total)
        item.append(type_values["FULL"])
        item.append(type_values["FROZEN"])
        item.append(type_values["AVAILABLE"])
        if total > 0:
            item.append(round(type_values["AVAILABLE"]/int(total)*100,0))
        else:
            item.append(0)
        out_csv.append(item)

    with open(args.tape_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(out_csv)

    logger.info('runout: get tape used successfull')
