#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-12-02 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import sys
import time

from nbu.check_log import *
from nbu.input_cmd import *
from nbu.input_json import *
from nbu.check_env import *
from nbu.check_disk import *
from nbu.check_tape import *
from nbu.check_jobs import *
from nbu.check_sum import *
from nbu.check_csv import *


if __name__ == '__main__':
   # choice select type
    if (param['input_type'] == 'cmd'):
        args=input_cmd.get_args(sys.argv[1:])
    elif (param['input_type'] == 'json'):
        args=input_json()

    if (args.sec):
        sec = args.sec
    else:
        sec = '600'

    master = args.master

    args.disk_list = work_dir + 'tmp/' + master + '_disk_' + date_day +'.txt'
    args.tape_list = work_dir + 'tmp/' + master + '_tape_' + date_day +'.txt'
    args.jobs_list = work_dir + 'tmp/' + master + '_bpdbjobs_' + date_day +'.txt'
    args.policy_list = work_dir + 'tmp/' + master + '_policy_' + date_day +'.txt'
    args.client_list = work_dir + 'tmp/' + master + '_client_' + date_day +'.txt'
    args.server_list = work_dir + 'tmp/' + master + '_server_' + date_day +'.txt'
    args.sum_csv = work_dir + 'csv/' + master + '_sum_' + date_day +'.csv'
    args.jobs_csv = work_dir + 'csv/' + master + '_jobs_' + date_day +'.csv'
    args.policy_csv = work_dir + 'csv/' + master + '_policy_' + date_day +'.csv'
    args.disk_csv = work_dir + 'csv/' + master + '_disk_' + date_day +'.csv'
    args.tape_csv = work_dir + 'csv/' + master + '_tape_' + date_day +'.csv'
    args.report_xlsx = work_dir + 'out/nbu_report_' + date_day +'.xlsx'

    if (args.opr == 'check_disk_used'):
        check_disk_used(args)

    if (args.opr == 'check_tape_used'):
        check_tape_used(args)

    if (args.opr == 'check_jobs_list'):
        check_jobs_list(args)

    if (args.opr == 'check_sum_used'):
        check_sum_used(args)

    if (args.opr == 'check_csv_excel'):
        check_csv_excel(args)
