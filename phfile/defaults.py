#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Defaults.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


DEFAULT_CHART_PARAMS = {
    0: {
        'contour': {'color': 'red', 'linestyle': '-'},
        'fill': {'alpha': .5, 'color': 'yellow', },
        'label': 'C0-C180',
    },
    1: {
        'contour': {'color': 'blue', 'linestyle': '-'},
        'fill': {'alpha': .5, 'color': 'yellow', },
        'label': 'C90-C270',
    },
}
DEFAULT_TEXT = {
    'horizontalalignment': 'center',
    'verticalalignment': 'center',
    'bbox': {'facecolor': 'white', 'edgecolor': 'black', },
}
