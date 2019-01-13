#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Tests for Photometry class.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


import copy
import unittest


from .. import IES


document = {
    'test': '2018-10-09',
    'testlab': 'AQLAB',
    'issuedate': '2018-10-09',
    'future_use': 1,
}


class TestPhotometry(unittest.TestCase):
    """."""

    def setUp(self):
        """."""
        self._ies_obj = IES()
        self._ies_obj._document = copy.deepcopy(document)

    def test_get_valid_item(self):
        """."""
        items = ['test', 'testlab', 'future_use']
        self.assertEqual(self._ies_obj.item(items[0]),
                         document[items[0]])
        self.assertEqual(self._ies_obj.item(*items),
                         {item: document[item]
                          for item in items})

    def test_get_fake_item(self):
        """."""
        fake_items = ['fake_item', 'another_fake_item']
        with self.assertWarns(UserWarning) as wn:
            result = self._ies_obj.item(*fake_items)
        self.assertEqual(set([str(warn.message) for warn in wn.warnings]),
                         set(['there is no item %s' % item
                              for item in fake_items]))
        self.assertEqual(False, result)

    def test_get_valid_and_fake_item(self):
        """."""
        items = ['test', 'testlab', 'fake_item', 'issuedate']
        with self.assertWarns(UserWarning) as wn:
            result = self._ies_obj.item(*items)
        self.assertEqual(str(wn.warnings[0].message),
                         'there is no item fake_item')
        self.assertEqual(result,
                         {key: value
                          for key, value in document.items()
                          if key in items})
