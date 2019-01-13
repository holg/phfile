#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Tests for IES class.

Method for setting items is more or less the same for LDT and IES classes,
tests are only for a bit more complexed method of LDT class.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


from unittest import mock
import unittest

from .test_data import (ldt_document_dict,
                        ldt_set_input_faulty,
                        ldt_set_input_valid,
                        ldt_text)
from .. import LDT


class TestLDT(unittest.TestCase):
    """."""

    def setUp(self):
        """."""
        document_dict = {
            'report_no': '2017-11-09/AQLAB',
            'luminaire_name': 'dioda LENS LINE 15st 3000K 250mA',
            'luminaire_no': '12345',
        }
        self._ldt_obj = LDT()
        self._ldt_obj.validate(document_dict, update=True)

    @mock.patch('builtins.open',
                new_callable=mock.mock_open,
                read_data=ldt_set_input_valid)
    def test_load_success(self, m):
        """."""
        self.assertEqual(bool(self._ldt_obj.load('path/to/ldt/file')),
                         True)

    @mock.patch('builtins.open',
                new_callable=mock.mock_open,
                read_data=ldt_set_input_faulty)
    def test_load_failed(self, m):
        """."""
        self.assertRaises(ValueError,
                          lambda: self._ldt_obj.load('path/to/ldt/file'))

    def test_set_valid_items_list_keys(self):
        """."""
        document_list = list(sum(ldt_document_dict.items(), ()))
        self._ldt_obj.set(*document_list)
        self.assertEqual(self._ldt_obj.item(*list(ldt_document_dict.keys())),
                         ldt_document_dict)

    def test_set_valid_items_list_indexes(self):
        """."""
        document_list = [
            8, ldt_document_dict['report_no'],
            9, ldt_document_dict['luminaire_name'],
            10, ldt_document_dict['luminaire_no'],
        ]
        self._ldt_obj.set(*document_list)
        self.assertEqual(self._ldt_obj.item(*list(ldt_document_dict.keys())),
                         ldt_document_dict)

    def test_set_valid_items_keywords_keys(self):
        """."""
        self._ldt_obj.set(**ldt_document_dict)
        self.assertEqual(self._ldt_obj.item(*list(ldt_document_dict.keys())),
                         ldt_document_dict)

    def test_set_valid_items_keywords_indexes(self):
        """."""
        self._ldt_obj.set(**{
            '8': ldt_document_dict['report_no'],
            '9': ldt_document_dict['luminaire_name'],
            '10': ldt_document_dict['luminaire_no'],
        })
        self.assertEqual(self._ldt_obj.item(*list(ldt_document_dict.keys())),
                         ldt_document_dict)

    def test_set_fake_item(self):
        """."""
        document_list = list(sum(ldt_document_dict.items(), ()))
        document_list.extend(['fake_item', 'fake_value'])
        with self.assertWarns(UserWarning) as wn:
            self._ldt_obj.set(*document_list)
        self.assertEqual(str(wn.warnings[0].message),
                         'there is no item fake_item')
        self.assertEqual(self._ldt_obj.item(*list(ldt_document_dict.keys())),
                         ldt_document_dict)

    def test_set_wrong_number_of_args(self):
        """."""
        self.assertRaises(TypeError,
                          lambda: self._ldt_obj.set(*['arg'+str(i)
                                                      for i
                                                      in range(1, 4)]))

    @mock.patch('builtins.open',
                new_callable=mock.mock_open,
                read_data=ldt_set_input_valid)
    def test_text(self, m):
        """."""
        self._ldt_obj.load('path/to/ldt/file')
        self.maxDiff = None
        self.assertEqual(ldt_text,
                         self._ldt_obj.text)
