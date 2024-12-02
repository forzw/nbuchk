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
import subprocess as sb
from nbu.check_env import *

def check_disk_used(args):

    logger.info('start get disk used')
    script_cmd = 'cat ' + args.disk_list

    logger.info('runcmd: '+ script_cmd)
    result = sb.run(script_cmd, shell=True, timeout=10, stdout=sb.PIPE, stderr=sb.PIPE)
    #logger.info(result.stdout.decode('utf-8'))

    if result.stderr:
        logger.error('runout: get disk used failed')
        logger.error(result.stderr.decode('utf-8'))

    out_csv = []
    for res_line in result.stdout.decode('utf-8').split('\n'):
        res_sp = res_line.split(' ')
        if len(res_sp) > 10:
            dp_name = res_sp[1]
            dp_id = res_sp[4]
            dp_size = res_sp[5]
            dp_free = res_sp[6]
            dp_used = res_sp[7]
            dp_used_per = round(float(dp_used)/float(dp_size)*100,0)
            #print(args.master,dp_name,dp_size,dp_used,dp_free,dp_used_per)
            if dp_used > param['water_low'] and dp_used < param['water_high']:
                logger.warn(dp_name + ' used is ' + dp_used)
            
            if dp_used >= param['water_high']:
                logger.error(dp_name + ' used is ' + dp_used)
            item = [args.master]
            item.append(dp_name)
            item.append(dp_size)
            item.append(dp_used)
            item.append(dp_free)
            item.append(dp_used_per)
            out_csv.append(item)

    with open(args.disk_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(out_csv)

    logger.info('runout: get disk used successfull')

