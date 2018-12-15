# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import os
import sys
import unittest
sys.path.append(os.getcwd())
from classcli import CliBuilder


class TestSingleClass(unittest.TestCase):

    class TestClass:
            callable_cls = True
            command = 'test'

            def _base(self):
                return 1

            def test_method(self):
                return 2

            def test_argument(self, arg1):
                return arg1

            def test_argument_type(self, arg1: int):
                return arg1

            def test_argument_opt(self, arg1='2'):
                return arg1

            def test_argument_opt_type(self, arg1: int=2):
                return arg1

            def test_argument_opt_multiple(self, arg1='2', barg='3'):
                return barg

            def test_argument_bool(self, arg1: bool):
                return arg1

            def test_argument_bool_false(self, arg1: bool=False):
                return arg1

    def setUp(self):
        self.parser = CliBuilder([TestSingleClass.TestClass, ])

    def test_base_func(self):
        self.assertEqual(self.parser.run_cli(['test', ]), 1)

    def test_non_base_func(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_method', ]), 2)

    def test_argument(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument', 3]), '3')

    def test_argument_type(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_type', 3]), 3)

    def test_argument_opt(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_opt', '--arg1', '1']), '1')

    def test_argument_opt_type(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_opt_type', '--arg1', '1']), 1)

    def test_argument_opt_alias(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_opt', '-a', '1']), '1')

    def test_argument_opt_multiple(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_opt_multiple', '-b', '2']), '2')

    def test_argument_bool(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_bool', '-arg1']), True)

    def test_argument_bool_false(self):
        self.assertEqual(self.parser.run_cli(['test', 'test_argument_bool_false', '-arg1']), False)
