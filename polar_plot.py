#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""PolarPlot.

Copyright (c) 2022 Holger Trahe trahe@mac.com

"""
import sys
from phfile import LDT


def polar_plot(in_ldc, out_plot):
    ldt_file = LDT()
    ldt_file.load(in_ldc)
    ldt_file.plot(out_plot)


if __name__ == '__main__':
    len_argv = len(sys.argv)
    if len_argv < 2:
        raise Exception('Need at least the input ldc file to plot')
    in_ldc = sys.argv[1]
    if len_argv > 2:
        out_plot = sys.argv[2]
    else:
        out_plot = in_ldc + '.svg'
    if in_ldc == '-h':
        print('./polar_plot in _ldc (optional out_plot, default: in_ldc.svg')
        exit()
    polar_plot(in_ldc, out_plot)

