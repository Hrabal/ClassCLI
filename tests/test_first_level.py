# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import os
import sys
import unittest
from subprocess import check_output


class BaseUnit(unittest.TestCase):
    def _call_cli(self, args, expected):
        r = check_output([sys.executable, 'tests/%s' % self.TEST_CLI, ] + args)
        self.assertEqual(r.decode('utf-8').strip(), expected)


class TestFirstLevel(BaseUnit):
    TEST_CLI = 't_%s' % '_'.join(__file__.split('/')[-1].split('_')[1:])

    def test_one_arg_base(self):
        self._call_cli(['test', ], 'test NOK')
