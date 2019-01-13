#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""LDT class.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


import matplotlib.pyplot as plt
import math
import numpy as np
import pathlib
import re

from .defaults import DEFAULT_CHART_PARAMS, DEFAULT_TEXT
from .phbase import PHBase
from .schemas import ldt_schema
from .utils import safe_filename


class LDT(PHBase, object):
    """Class for handling ies data.

    Raises --
        TypeError: in case of wrong number of arguments passed to set() method
        ValidationError: in case of attempt to write file with incorrect
            or incomplete data.
        ValueError: in case of incorrect ldt file

    """

    def __init__(self):
        """Class constructor."""
        def to_int(val):
            result = re.search('[0-9]{2,4}', val)
            return int(result[0]) if result else 0

        super().__init__()
        self.schema = ldt_schema

    @property
    def text(self):
        """Return content of ldt file.

        Returns --
            (str): ies document
        """
        def to_str(item):
            try:
                return '\n'.join([to_str(i.values()) for i in item])
            except AttributeError:
                return ('\n'.join(map(str, item)))

        self.validate(self.document)
        results = [self.document[item]
                   if not isinstance(self.document[item], list)
                   else to_str(self.document[item])
                   for item in self.schema.keys()]
        return '\n'.join(map(str, results))

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

    def load(self, ldt_path):
        """Load ldt file.

        Args:
            ldt_path (str): path to ldt file

        Returns --
            (obj): self
        """
        class _Index(object):
            __slots__ = (
                '_index',
            )

            def __init__(self, index):
                self._index = index

            @property
            def i(self):
                return self._index

            def add(self, val):
                self._index += val
                return self._index

        keys = list(self.schema.keys())[:26]
        with open(ldt_path) as f:
            items = f.read().splitlines()
            document = {keys[i]: items[i]
                        for i in range(0, 26)}
            # auxiliary variables for storing keys of lamp data dict
            keys = list(self.schema
                        ['lamps']
                        ['schema']
                        ['schema'].keys())
            i = _Index(26)
            # generates list od dicts with lamps data
            document.update({
                'lamps': [{keys[j]: item
                           for j, item
                           in enumerate(items[i.i:i.add(6)])}
                          for k in range(0, int(items[25]))],
            })
            document.update({
                'direct_ratios': items[i.i:i.add(10)],
            })
            number_mc = int(items[3])
            document.update({
                'angles_c': items[i.i:i.add(number_mc)],
            })
            number_ng = int(items[5])
            document.update({
                'angles_g': items[i.i:i.add(number_ng)],
            })
            # calculates mc1, mc2 according to Note 2 from
            # http://www.helios32.com/Eulumdat.htm
            mc1, mc2 = {
                0: (1, number_mc),
                1: (1, 1),
                2: (1, number_mc // 2 + 1),
                3: (3 * number_mc // 4 + 1, 5 * number_mc // 4 + 1),
                4: (1, number_mc // 4 + 1),
            }.get(int(items[2]))
            document.update({
                'luminous_intensities': items[i.i:i.add((mc2 - mc1 + 1)
                                              * number_ng)],
            })
        if i.i != len(items):
            raise ValueError(('ldt file has wrong number of lines'
                              + ' (got %s expected %s)')
                             % (len(items), i.i))
        self.validate(document)
        return self

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
        def _args(*args):
            return [keys[args[i] - 1]
                    if isinstance(args[i], int)
                    and args[i] >= 0
                    and args[i] <= 30
                    and i % 2 != 1
                    else args[i] for i in range(0, len(args))]

        def _kwargs(**kwargs):
            return {(keys[int(key) - 1]
                     if re.search((r'^([1-9]{1})$|'
                                   r'^([12]{1}[0-9]{1})$|'
                                   r'^(3{1}[01]{1})$'), key)
                    else key): value
                    for key, value in kwargs.items()}

        keys = list(self.schema.keys())
        args = _args(*args)
        kwargs = _kwargs(**kwargs)
        super().set(*args, **kwargs)
        return self

    def plot(self, save_path='', **kwargs):
        """Plot luminescence chart.

        Args:
            save_path (obj, optional): path to output svg file
            **kwargs: optional keyword arguments for styling plot

        Returns ---
            str: path to output svg file
        """
        def c_plane_intensities(*args):
            try:
                start, end = (args[0] // self.document['distance_dc']
                              * self.document['number_ng'],
                              (args[0] // self.document['distance_dc'] + 1)
                              * self.document['number_ng'])
            except ZeroDivisionError:
                start, end = (0, self.document['number_ng'])
            return self.document['luminous_intensities'][start:end]\
                if self.document['luminous_intensities'][start:end]\
                else c_plane_intensities(*args[1:])

        def round_up(num, oom=1):
            digits = list(reversed([int((num // 10 ** i) % 10)
                                    for i
                                    in range(math.floor(math.log10(num)),
                                             -1, -1)]))
            return sum([digits[i] * 10 ** i
                        if i != oom
                        else (digits[i] + 1) * 10 ** i
                        for i in range(oom, len(digits))])\
                if num > 10 ** oom else 10 ** oom

        self.validate(self.document)
        # overwrite default rcParams
        plt.rcParams.update(kwargs.get('rc', {}))
        fig = plt.figure()
        ax = fig.add_axes([0, .15, 1, .75],
                          projection='polar',
                          rlabel_position=22.5,
                          theta_offset=(-np.pi / 2))
        theta = list(map(lambda x: x * np.pi / 180,
                         [i * self.document['distance_dg']
                          for i in range(0, 2 * self.document['number_ng'])]))
        ax.set_thetagrids(**kwargs.get('thetagrids',
                                       {'angles': [i
                                                   for i
                                                   in range(0, 360, 30)]}))
        c_planes = [(0, 180)]
        if self.document['symmetry_indicator'] != 1:
            c_planes.extend([(90, 270)])
        for i, (c_pf, c_ps) in enumerate(c_planes):
            values = c_plane_intensities(c_pf)\
                     + list(reversed(c_plane_intensities(c_ps, c_pf)))
            chart_params = kwargs.get({
                0: 'C0C180',
                1: 'C90C270',
            }.get(i, {}), DEFAULT_CHART_PARAMS.get(i, {}))
            ax.fill(theta,
                    values,
                    **chart_params.get('fill', {}))
            ax.plot(theta, values,
                    label=chart_params.get('label',
                                           '-'.join(map(lambda x: 'C' + str(x),
                                                    [c_pf, c_ps]))),
                    **chart_params.get('contour', {}))
        if ax.get_rmax() > 100:
            rmax = round_up(ax.get_rmax(), 2)
        else:
            rmax = round_up(ax.get_rmax())
        ax.set_rmax(rmax)
        ax.set_rticks([i * rmax / kwargs.get('rticks.num', 4)
                       for i in range(0, kwargs.get('rticks.num', 4) + 1)])
        ax.set_yticklabels([])
        fig.legend(**kwargs.get('legend', {}))
        ax.text(3 * np.pi / 2,
                rmax,
                '%s cd/klm' % str(rmax),
                **kwargs.get('text', DEFAULT_TEXT))
        if not save_path:
            save_path = safe_filename(self.document.get('luminaire_name',
                                                        'none'),
                                      'svg')
        plt.savefig(save_path)
        plt.close(fig)
        return self

    def write(self, save_path=''):
        """Write ldt file.

        Args:
            save_path (obj, optional): path to output ldt file

        Returns --
            str: path to output ldt file
        """
        if not save_path:
            save_path = safe_filename(self.document.get('luminaire_name',
                                                        'none'),
                                      'ldt')
        ldt_file = open(pathlib.Path(save_path), 'w')
        ldt_file.write(self.text)
        ldt_file.close()
        return self
