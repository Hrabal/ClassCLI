# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import os
import sys
import unittest
import argparse
sys.path.append(os.getcwd())
from classcli import CliBuilder


class TestClass:
    callable_cls = True
    command = 'test'

    def _base(self):
        pass


class TestInit(unittest.TestCase):
    def test_from_list(self):
        inst = CliBuilder([TestClass, ])
        self.assertIsInstance(inst.parser, argparse.ArgumentParser)

    def test_from_dict(self):
        inst = CliBuilder({'test_class': TestClass})
        self.assertIsInstance(inst.parser, argparse.ArgumentParser)

    def test_from_module(self):
        from tests import module
        inst = CliBuilder(module)
        self.assertIsInstance(inst.parser, argparse.ArgumentParser)
