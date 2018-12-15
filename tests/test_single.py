# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from contextlib import redirect_stdout
from io import StringIO

from tests.module import TestClass
from classcli import CliBuilder


class TestSingleClass(unittest.TestCase):

    def setUp(self):
        self.parser = CliBuilder([TestClass, ])

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

    def test_no_args(self):
        out = StringIO()
        with redirect_stdout(out):
            self.parser.run_cli([])
        output = out.getvalue()
        self.assertTrue('At least one argument needed.' in output)
