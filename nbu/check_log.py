#!/usr/bin/env python
# _*_ coding:utf-8 _*_
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# write by : kevin chen
# version : 1.0
# update : 2024-12-01 create scripts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import logging

class logger:
    def __init__(self, cmd, filename, screenlog=False):
        self.logger = logging.getLogger(cmd)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
        #fmt = logging.Formatter('%(asctime)s %(levelname)5s %(message)s', '%H:%M:%S')
        screen = logging.StreamHandler()
        screen.setFormatter(fmt)
        if screenlog:
            screen.setLevel(logging.DEBUG)
        else:
            screen.setLevel(logging.INFO)
        self.logger.addHandler(screen)

        logfile = logging.FileHandler(filename)
        logfile.setLevel(logging.DEBUG)
        logfile.setFormatter(fmt)
        self.logger.addHandler(logfile)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)