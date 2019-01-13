#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Validation schemas.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


import re


def _to_int(val):
    result = re.search('[0-9]{2,4}', val)
    return int(result[0]) if result else 0


_ldt_lamp_schema = {
    'number_of': {
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'type_of': {
        'required': True,
        'type': 'string',
    },
    'total_flux': {
        'coerce': (float, int),
        'required': True,
        'type': 'integer',
    },
    'color_temp': {
        'coerce': (str, _to_int),
        'default': 3000,
        'max': 6500,
        'min': 2400,
        'required': True,
        'type': 'integer',
    },
    'cri': {
        'coerce': (str, _to_int),
        'default': 80,
        'required': True,
        'max': 100,
        'min': 0,
        'type': 'integer',
    },
    'total_power': {
        'coerce': float,
        'required': True,
        'type': 'float',
    },
}

ldt_schema = {
    'company': {  # 1
        'required': True,
        'type': 'string',
    },
    'type_indicator': {  # 2
        'coerce': int,
        'max': 3,
        'min': 1,
        'required': True,
        'type': 'integer',
    },
    'symmetry_indicator': {  # 3
        'coerce': int,
        'max': 4,
        'min': 1,
        'required': True,
        'type': 'integer',
    },
    'number_mc': {  # 4
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'distance_dc': {  # 5
        'coerce': (str, _to_int),
        'required': True,
        'type': 'integer',
    },
    'number_ng': {  # 6
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'distance_dg': {  # 7
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'report_no': {  # 8
        'required': True,
        'type': 'string',
    },
    'luminaire_name': {  # 9
        'required': True,
        'type': 'string',
    },
    'luminaire_no': {  # 10
        'required': True,
        'type': 'string',
    },
    'file_name': {  # 11
        'required': True,
        'type': 'string',
    },
    'date_user': {  # 12
        'required': True,
        'type': 'string',
    },
    'luminaire_length': {  # 13
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'luminaire_width': {  # 14
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'luminaire_height': {  # 15
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'luminous_length': {  # 16
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'luminous_width': {  # 17
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'luminous_height_c0': {  # 18
        'coerce': float,
        'default': 0.0,
        'required': True,
        'type': 'float',
    },
    'luminous_height_c90': {  # 19
        'coerce': float,
        'default': 0.0,
        'required': True,
        'type': 'float',
    },
    'luminaire_height_c180': {  # 20
        'coerce': float,
        'default': 0.0,
        'required': True,
        'type': 'float', },
    'luminaire_height_c270': {  # 21
        'coerce': float,
        'default': 0.0,
        'required': True,
        'type': 'float',
    },
    'dff': {  # 22
        'coerce': float,
        'default': 100,
        'max': 100,
        'min': 0,
        'required': True,
        'type': 'float',
    },
    'lorl': {  # 23
        'coerce': float,
        'max': 100,
        'min': 0,
        'required': True,
        'type': 'float',
    },
    'conversion_factor': {  # 24
        'coerce': float,
        'max': 1,
        'min': 0,
        'required': True,
        'type': 'float',
    },
    'tilt': {  # 25
        'coerce': float,
        'max': 90,
        'min': 0,
        'required': True,
        'type': 'float',
    },
    'number_n': {  # 26
        'coerce': int,
        'default': 1,
        'type': 'integer',
    },
    'lamps': {
        'required': True,
        'schema': {  # 26a-f
            'type': 'dict',
            'schema': _ldt_lamp_schema,
            'required': True,
        },
        'type': 'list',
    },
    'direct_ratios': {
        'required': True,
        'schema': {  # 27
            'coerce': float,
            'required': True,
            'type': 'float',
        },
        'type': 'list',
    },
    'angles_c': {  # 28
        'required': True,
        'schema': {
            'coerce': float,
            'required': True,
            'type': 'float',
        },
        'type': 'list',
    },
    'angles_g': {  # 29
        'required': True,
        'schema': {
            'coerce': float,
            'required': True,
            'type': 'float',
        },
        'type': 'list', },
    'luminous_intensities': {  # 30
        'required': True,
        'schema': {
            'coerce': float,
            'required': True,
            'type': 'float',
        },
        'type': 'list',
    },
}

ies_schema = {
    'header': {
        'default': 'IESNA:LM-63-2002',
        'required': True,
        'type': 'string',
    },
    'test': {
        'required': True,
        'type': 'string',
    },
    'testlab': {
        'required': True,
        'type': 'string',
    },
    'issuedate': {
        'required': True,
        'type': 'string',
    },
    'manufac': {
        'required': True,
        'type': 'string',
    },
    'lumcat': {
        'required': True,
        'type': 'string',
    },
    'luminaire': {
        'required': True,
        'type': 'string',
    },
    'lampcat': {
        'required': True,
        'type': 'string',
    },
    'lamp': {
        'required': True,
        'type': 'string',
    },
    'number_of_lamps': {
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'lumens_per_lamp': {
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'candela_multiplier': {
        'coerce': float,
        'default': 1,
        'required': True,
        'type': 'float',
    },
    'number_of_vertical_angles': {
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'number_of_horizontal_angles': {
        'coerce': int,
        'required': True,
        'type': 'integer',
    },
    'photometric_type': {
        'coerce': int,
        'default': 1,
        'max': 3,
        'min': 1,
        'required': True,
        'type': 'integer',
    },
    'units_type': {
        'coerce': int,
        'default': 2,
        'max': 2,
        'min': 1,
        'required': True,
        'type': 'integer',
    },
    'width': {
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'length': {
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'height': {
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'ballast_factor': {
        'coerce': float,
        'default': 1,
        'required': True,
        'type': 'float',
    },
    'future_use': {
        'allowed': [1],
        'coerce': int,
        'default': 1,
        'required': True,
        'type': 'integer',
    },
    'input_watts': {
        'coerce': float,
        'required': True,
        'type': 'float',
    },
    'vertical_angles': {
        'required': True,
        'type': 'list',
        'schema': {
            'coerce': float,
            'required': True,
            'type': 'float',
        },
    },
    'horizontal_angles': {
        'required': True,
        'type': 'list',
        'schema': {
            'coerce': float,
            'required': True,
            'type': 'float',
        },
    },
    'candela_values': {
        'required': True,
        'type': 'list',
        'schema': {
            'coerce': float,
            'required': True,
            'type': 'float',
        },
    },
}
