#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-12-01 create scripts
# update : 2022-12-01 sync jobs with active
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import json
import os
import datetime
import subprocess as sb
from nbu.check_env import *


def read_and_parse_json(file_path):
  try:
    with open(file_path, 'r') as f:
      data = json.load(f)
      return data
  except FileNotFoundError:
    print(f"File '{file_path}' not found.")
    return "None"
  except json.JSONDecodeError:
    print(f"File '{file_path}' read failed.")
    return "None"

def unixtime_to_beijing_time(unix_timestamp):
  dt_obj = datetime.datetime.fromtimestamp(unix_timestamp)
  beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
  dt_obj = dt_obj.astimezone(beijing_tz)
  beijing_time_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
  return beijing_time_str


def check_jobs_list(args):

    jobs_data = read_and_parse_json(args.jobs_list)
    out_csv = []
    i_num = 0
    for jobs in jobs_data:       
        try:
            if jobs['JobTypeText'] == 'Backup':
                item = [args.master]
                item.append(jobs['JobId'])
                item.append(jobs['JobTypeText'])
                item.append(jobs['BackupId'])
                item.append(jobs['PolicyName'])
                item.append(jobs['PolicyTypeText'])
                item.append(jobs['ClientName'])
                item.append(jobs['ScheduleName'])
                if 'KilobytesTransferred' in jobs:
                    item.append(jobs['KilobytesTransferred'])
                else:
                    item.append(0)
                item.append(unixtime_to_beijing_time(jobs['StartTime']))
                if str(jobs['EndTime']) == '0':
                   item.append('0')
                else:
                   item.append(unixtime_to_beijing_time(jobs['EndTime']))
                item.append(jobs['Status'])
                item.append(jobs['StateText'])
                out_csv.append(item)
                i_num += 1
        except:
            pass



    with open(args.jobs_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(out_csv)

    logger.info('get jobs count : '+ str(i_num))

