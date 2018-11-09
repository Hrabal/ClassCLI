# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import os
import sys
sys.path.append(os.getcwd())

from classcli import CliBuilder


class Test:
    callable_cls = True
    command = 'test'

    def _base(self):
        print('test OK')


if __name__ == '__main__':
    CliBuilder(locals()).run_cli()
