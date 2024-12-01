#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-10-24 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import json
import datetime
from nbu.check_log import *

#defined readonly variable

nbdevquery = "/usr/openv/netbackup/bin/admincmd/nbdevquery"

#defined variable
work_dir = "/usr/openv/scripts/nbuchk/"
#date_day = datetime.date.today().strftime("%Y%m%d")
date_day = "20241022"


global param
with open(work_dir + 'config.json') as handle:
    param = json.loads(handle.read())

global logger
logger = logger('run', param['run_log'], param['verbose'])
