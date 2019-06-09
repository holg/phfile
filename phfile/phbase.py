#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Handles photometric data.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


import abc
import warnings

import cerberus

from .exceptions import PhotometryValidationError


class PHBase(abc.ABC, object):
    """Abstract class for handling photometric data."""

    __slots__ = (
        '_document',
        '_validator',
    )

    def __init__(self):
        """Class constructor."""
        self._document = {}
        self._validator = cerberus.Validator()

    @property
    def document(self):
        """Return document.

        Returns --
            (dict): document
        """
        return self._document

    @property
    def errors(self):
        """Return validation errors.

        Returns --
            (list): validation errors
        """
        return self._validator.errors

    @property
    def schema(self):
        """Return document schema.

        Returns --
            (dict): schema
        """
        return self._validator.schema

    @schema.setter
    def schema(self, schema):
        """."""
        self._validator.schema = schema

    @property
    @abc.abstractmethod
    def text(self):
        """Return content of ies file.

        Returns --
            (str): ies document
        """
        pass

    @abc.abstractmethod
    def item(self, *args):
        """Return items.

        Args:
            *args: variable length argument list with requested items names

        Returns --
            ies items, in case of few requested items results are returned
            as dictionary, single item is returned as value, in case of
            not finding the item False is returned
        """
        results = {arg: self.document.get(arg, None)
                   for arg in args
                   if arg in self.schema}
        for item in set(args).difference(list(results.keys())):
            warnings.warn('there is no item %s' % item)
        if results:
            return next(iter(results.values())) if len(results) == 1\
                else results
        else:
            return False

    @abc.abstractmethod
    def set(self, *args, **kwargs):
        """Set value of items.

        Values given as keyword arguments have higher priority than those
        given in argument list. For the item given in both ways only value
        from keyword arguments will matter.

        Args:
            *args: variable length argument list, odd number of arguments is
            required eg. *['1st_item_name', '1st_item_value', '2nd_item_name',
            '2nd_item_value', 'nth_item_name', 'nth_item_value']
            **kwargs: arbitrary keyword arguments
        """
        def handle(**kwargs):
            for item, value in kwargs.items():
                getattr(self, '_handle_' + item)(value)

        def sift(**kwargs):
            for item in set(list(kwargs.keys()))\
                        .difference(list(self.schema.keys())
                                    + handlers):
                warnings.warn('there is no item %s' % item)
                del kwargs[item]
            return kwargs

        # before update checks number of args, skips unknown items
        # and raises warnings
        if args and len(args) != 2 and len(args) % 2 != 0:
            raise TypeError('set() method takes even number of arguments'
                            + ' (odd number given)')
        handlers = [func[8:] for func in dir(self)
                    if func.startswith('_handle_')]
        kwargs = sift(**{**{args[i]: args[i+1]
                            for i in range(0, len(args), 2)},
                         **kwargs})
        handle(**{item: value for item, value in kwargs.items()
                  if item in handlers})
        self.validate(kwargs, update=True)

    def validate(self, document, update=False):
        """Validate document.

        Args:
            document (dict): document for validation
        """
        self._validator.validate({item: value
                                  for item, value in document.items()
                                  if item in self.schema},
                                 update=update)
        if not self.errors:
            # condition 'item in kwargs' is neccessary due to some items
            # to have default values defined in validation schema,
            # defaults are used for items not present in kwargs and
            # can overwrite correct values set or loaded earlier
            self._document.update({
                item: value
                for item, value in self._validator.document.items()
                if item in document
            })
        else:
            if update:
                raise PhotometryValidationError('input data seems to be'
                                                + ' incorrect')
            else:
                raise PhotometryValidationError('input data seems to be'
                                                + ' incomplete or incorrect')
