#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""IES class.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


from .phbase import PHBase
from .schemas import ies_schema


class IES (PHBase, object):
    """Class for handling ies data.

    Raises --
        TypeError: in case of wrong number of arguments passed to set() method
        ValueError: in case of wrong number of candela values
            or vertical / horizontal angles

    """

    __slots__ = (
        '_template',
    )

    def __init__(self):
        """Class constructor."""
        super().__init__()
        # TILT other than NONE is not supported
        self._template = (
            '{header}\n'
            '[TEST] {test}\n'
            '[TESTLAB] {testlab}\n'
            '[ISSUEDATE] {issuedate}\n'
            '[MANUFAC] {manufac}\n'
            '[LUMCAT] {lumcat}\n'
            '[LUMINAIRE] {luminaire}\n'
            '[LAMPCAT] {lampcat}\n'
            '[LAMP] {lamp}\n'
            'TILT=NONE\n'
            '{number_of_lamps} {lumens_per_lamp} {candela_multiplier}'
            ' {number_of_vertical_angles} {number_of_horizontal_angles}'
            ' {photometric_type} {units_type} {width} {length} {height}\n'
            '{ballast_factor} {future_use} {input_watts}\n'
            '{vertical_angles}\n'
            '{horizontal_angles}\n'
            '{candela_values}'
        )
        self.schema = ies_schema

    @property
    def text(self):
        """Return content of ies file.

        Returns --
            (str): ies document
        """
        def to_str(value):
            return str(value) if not isinstance(value, list)\
                else ' '.join(map(str, value))

        self.validate(self.document)
        result = self._template
        for item in self.document.keys():
            result = result.replace('{'+item+'}',
                                    to_str(self.document[item]))
        return result

    def item(self, *args):
        """Return items.

        Args:
            *args: variable length argument list with requested items names

        Returns --
            ies items, in case of few requested items results are returned
            as dictionary, single item is returned as value, in case of
            not finding the item False is returned
        """
        return super().item(*args)

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
        super().set(*args, **kwargs)
        return self
