#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-10-24 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
import argparse

class input_cmd:
    def get_args(self):
        parser = argparse.ArgumentParser(description='collect netbackup info')

        parser.add_argument('--master',metavar='master', required=False, action='store',help='master name')
        parser.add_argument('--opr',metavar='opr', required=True, action='store',help='opr method')
        parser.add_argument('--sec',metavar='sec', action='store',help='second ago')
        parser.add_argument('--file',metavar='file', action='store',help='file path')
        parser.add_argument('--preview', dest='preview', action='store_true',help='preview mode')
        parser.add_argument('--verbose', dest='verbose', action='store_true',help='verbose mode')

        args = parser.parse_args()
        return args
