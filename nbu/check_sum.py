#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-12-01 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import csv
import datetime
import subprocess as sb
from nbu.check_env import *


def check_characters_in_text(text1_path, text2_path):
    results = []
    with open(text1_path, 'r') as f1, open(text2_path, 'r') as f2:
        text2_chars = set(f2.read())
        for line in f1:
            line = line.replace('\n','')
            line_chars = set(line.strip())
            if line_chars.issubset(text2_chars):
                #logger.info('found backup jobs with policy: ' + line)
                pass
            else:
                logger.info('not found backup jobs with policy: ' + line)
                results.append(line)

    return results

def count_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"File: '{file_path}' not found.")
        return -1

def count_rows_with_char(csv_file, char, column_index=10):
    count = 0
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if char in row[column_index - 1]:
                    count += 1
        return count
    except FileNotFoundError:
        return -1

def count_rows_not_char(csv_file, char, column_index=10):
    count = 0
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if char not in row[column_index - 1]:
                    count += 1
        return count
    except FileNotFoundError:
        return -1



def check_sum_used(args):

    logger.info('start get policy not backup list')

    out_csv = []
    policy_not_jobs = ''

    try:
        policy_not_jobs = check_characters_in_text(args.policy_list, args.jobs_csv)
    except:
        pass

    for line in policy_not_jobs:
        item = [args.master]
        item.append(line)
        out_csv.append(item)
    
    with open(args.policy_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(out_csv)

    logger.info('runout: get policy not backup list successfull')


    policy_count = count_lines(args.policy_list)
    client_count = count_lines(args.client_list)
    server_count = count_lines(args.server_list)
    jobs_count = count_lines(args.jobs_csv)
    #print(policy_count,client_count,server_count)
    
    try:
        jobs_success = count_rows_with_char(args.jobs_csv, '0', 12)
        jobs_active = count_rows_with_char(args.jobs_csv, 'Active', 13)
        jobs_failed = count_rows_not_char(args.jobs_csv, '0', 12)
    except FileNotFoundError as e:
        print(f"Error {e}")

    jobs_success_per = 0
    if jobs_count > 0:
       jobs_success_per = round(int(jobs_success)/int(jobs_count)*100,0)

    #print(jobs_count,jobs_success,jobs_failed,jobs_active,jobs_success_per)

    today = datetime.date.today()
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    out_csv = []
    item = [args.master]
    item.append(yesterday_str + ' 08:00:00')
    item.append(today_str + ' 08:00:00')
    item.append(server_count)
    item.append(client_count)
    item.append(policy_count)
    item.append(jobs_count)
    item.append(jobs_success)
    item.append(jobs_failed)
    item.append(jobs_active)
    item.append(jobs_success_per)
    out_csv.append(item)


    with open(args.sum_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(out_csv)

    logger.info('runout: get nbu sum successfull')

