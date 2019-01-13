#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Minor tools.

Copyright (c) 2018 Przemysław Kaliś przemek.kalis@gmail.com

"""


def safe_filename(str, ext):
    """Safe file name.

    Args:
        str (str): proposed file name
        ext (str): extension

    Returns --
        str: safe file name
    """
    return ''.join([c
                    if c.isalnum() or c == ' '
                    else '_' for c in str]) + '.' + ext
