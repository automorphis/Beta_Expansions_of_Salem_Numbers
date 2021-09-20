"""
    Beta Expansions of Salem Numbers, calculating periods thereof
    Copyright (C) 2021 Michael P. Lane

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""

from enum import Enum

from numpy.polynomial.polynomial import Polynomial

_boyd = [
    ( (1,   0,  -4,  -7,  -4,   0, 1), (       1,       60) ),
    ( (1,   0,  -2,  -3,  -2,   0, 1), (       1,        7) ),
    ( (1,   0,  -1,  -1,  -1,   0, 1), (       1,        7) ),
    ( (1,   0,  -1,  -2,  -1,   0, 1), (       1,        7) ),
    ( (1,  -1,  -7, -11,  -7,  -1, 1), (    2438,      863) ),
    ( (1,  -1,  -5,  -7,  -5,  -1, 1), (       1,       13) ),
    ( (1,  -1,  -4,  -5,  -4,  -1, 1), (       1,       27) ),
    ( (1,  -1,  -4,  -6,  -4,  -1, 1), (       1,       22) ),
    ( (1,  -1,  -3,  -3,  -3,  -1, 1), (       1,       35) ),
    ( (1,  -1,  -3,  -4,  -3,  -1, 1), (       1,       11) ),
    ( (1,  -1,  -3,  -5,  -3,  -1, 1), (       1,       20) ),
    ( (1,  -1,  -2,  -1,  -2,  -1, 1), (       7,       42) ),
    ( (1,  -1,  -2,  -3,  -2,  -1, 1), (      10,       22) ),
    ( (1,  -1,  -2,  -4,  -2,  -1, 1), (       1,       24) ),
    ( (1,  -1,  -1,   1,  -1,  -1, 1), (       1,       11) ),
    ( (1,  -1,  -1,   0,  -1,  -1, 1), (       1,        5) ),
    ( (1,  -1,  -1,  -1,  -1,  -1, 1), (       1,        5) ),
    ( (1,  -1,  -1,  -3,  -1,  -1, 1), (      12,       11) ),
    ( (1,  -1,   0,  -1,   0,  -1, 1), (       1,        5) ),
    ( (1,  -2, -11, -17, -11,  -2, 1), (       1,       31) ),
    ( (1,  -2, -10, -15, -10,  -2, 1), (       1,       39) ),
    ( (1,  -2,  -9, -14,  -9,  -2, 1), (       1,       23) ),
    ( (1,  -2,  -8, -11,  -8,  -2, 1), (       1,       13) ),
    ( (1,  -2,  -7,  -9,  -7,  -2, 1), (      27,       49) ),
    ( (1,  -2,  -7, -10,  -7,  -2, 1), (       1,       93) ),
    ( (1,  -2,  -6,  -7,  -6,  -2, 1), (       1,       27) ),
    ( (1,  -2,  -6,  -8,  -6,  -2, 1), (       7,       31) ),
    ( (1,  -2,  -6,  -9,  -6,  -2, 1), (     157,       88) ),
    ( (1,  -2,  -5,  -5,  -5,  -2, 1), (       1,       35) ),
    ( (1,  -2,  -5,  -6,  -5,  -2, 1), (       1,       11) ),
    ( (1,  -2,  -5,  -7,  -5,  -2, 1), (       1,       11) ),
    ( (1,  -2,  -5,  -8,  -5,  -2, 1), (       1,       20) ),
    ( (1,  -2,  -4,  -3,  -4,  -2, 1), (       1,       17) ),
    ( (1,  -2,  -4,  -5,  -4,  -2, 1), (       7,       92) ),
    ( (1,  -2,  -4,  -6,  -4,  -2, 1), (       1,       11) ),
    ( (1,  -2,  -4,  -7,  -4,  -2, 1), (       1,       24) ),
    ( (1,  -2,  -3,  -1,  -3,  -2, 1), (       1,       13) ),
    ( (1,  -2,  -3,  -2,  -3,  -2, 1), (       1,        9) ),
    ( (1,  -2,  -3,  -3,  -3,  -2, 1), (       1,        9) ),
    ( (1,  -2,  -3,  -5,  -3,  -2, 1), (      97,       49) ),
    ( (1,  -2,  -3,  -6,  -3,  -2, 1), (       1,       24) ),
    ( (1,  -2,  -2,   1,  -2,  -2, 1), (       1,       17) ),
    ( (1,  -2,  -2,   0,  -2,  -2, 1), (       1,        5) ),
    ( (1,  -2,  -2,  -1,  -2,  -2, 1), (       1,        5) ),
    ( (1,  -2,  -2,  -2,  -2,  -2, 1), (       1,        5) ),
    ( (1,  -2,  -2,  -3,  -2,  -2, 1), (       1,       20) ),
    ( (1,  -2,  -2,  -5,  -2,  -2, 1), (       5,       80) ),
    ( (1,  -2,  -1,   3,  -1,  -2, 1), (       1,        9) ),
    ( (1,  -2,  -1,   2,  -1,  -2, 1), (       1,        7) ),
    ( (1,  -2,  -1,   0,  -1,  -2, 1), (       1,        5) ),
    ( (1,  -2,  -1,  -2,  -1,  -2, 1), (       1,        5) ),
    ( (1,  -2,  -1,  -3,  -1,  -2, 1), (       1,       14) ),
    ( (1,  -2,   0,   1,   0,  -2, 1), (       1,        8) ),
    ( (1,  -2,   0,  -1,   0,  -2, 1), (       1,        5) ),
    ( (1,  -2,   0,  -2,   0,  -2, 1), (       1,        5) ),
    ( (1,  -2,   0,  -3,   0,  -2, 1), (       1,       12) ),
    ( (1,  -2,   1,  -2,   1,  -2, 1), (       1,        6) ),
    ( (1,  -2,   2,  -3,   2,  -2, 1), (       1,       10) ),
    ( (1,  -3, -15, -23, -15,  -3, 1), (       1,       35) ),
    ( (1,  -3, -14, -21, -14,  -3, 1), (       1,      218) ),
    ( (1,  -3,  -5,  -4,  -5,  -3, 1), (       1,        9) ),
    ( (1,  -3,  -5,  -5,  -5,  -3, 1), (       1,        9) ),
    ( (1,  -3,  -5,  -7,  -5,  -3, 1), (      76,       20) ),
    ( (1,  -3,  -5,  -8,  -5,  -3, 1), (       1,       11) ),
    ( (1,  -3,  -5,  -9,  -5,  -3, 1), (       1,       24) ),
    ( (1,  -3,  -4,  -1,  -4,  -3, 1), (       1,       13) ),
    ( (1,  -3,  -4,  -2,  -4,  -3, 1), (       1,        9) ),
    ( (1,  -3,  -4,  -3,  -4,  -3, 1), (       1,        9) ),
    ( (1,  -3,  -4,  -4,  -4,  -3, 1), (       1,        9) ),
    ( (1,  -3,  -4,  -5,  -4,  -3, 1), (       1,       20) ),
    ( (1,  -3,  -4,  -7,  -4,  -3, 1), (      31,       61) ),
    ( (1,  -3,  -4,  -8,  -4,  -3, 1), (       5,       33) ),
    ( (1,  -3,  -3,   1,  -3,  -3, 1), (       1,       17) ),
    ( (1,  -3,  -3,   0,  -3,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -3,  -1,  -3,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -3,  -2,  -3,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -3,  -3,  -3,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -3,  -4,  -3,  -3, 1), (       1,       20) ),
    ( (1,  -3,  -3,  -5,  -3,  -3, 1), (       1,       20) ),
    ( (1,  -3,  -3,  -7,  -3,  -3, 1), (       5,       80) ),
    ( (1,  -3,  -2,   3,  -2,  -3, 1), (       8,       37) ),
    ( (1,  -3,  -2,   2,  -2,  -3, 1), (       1,       13) ),
    ( (1,  -3,  -2,   0,  -2,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -2,  -1,  -2,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -2,  -3,  -2,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -2,  -4,  -2,  -3, 1), (       1,       14) ),
    ( (1,  -3,  -2,  -5,  -2,  -3, 1), (       1,       14) ),
    ( (1,  -3,  -1,   5,  -1,  -3, 1), (       1,       12) ),
    ( (1,  -3,  -1,   4,  -1,  -3, 1), (       1,        9) ),
    ( (1,  -3,  -1,   3,  -1,  -3, 1), (       1,        7) ),
    ( (1,  -3,  -1,   2,  -1,  -3, 1), (       1,        7) ),
    ( (1,  -3,  -1,   1,  -1,  -3, 1), (       1,        7) ),
    ( (1,  -3,  -1,  -1,  -1,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -1,  -2,  -1,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -1,  -3,  -1,  -3, 1), (       1,        5) ),
    ( (1,  -3,  -1,  -4,  -1,  -3, 1), (       1,       14) ),
    ( (1,  -3,  -1,  -5,  -1,  -3, 1), (       1,       12) ),
    ( (1,  -3,  -1,  -7,  -1,  -3, 1), (      -1,       -1) ),
    ( (1,  -3,   0,   2,   0,  -3, 1), (       1,        8) ),
    ( (1,  -3,   0,   1,   0,  -3, 1), (       1,        8) ),
    ( (1,  -3,   0,   0,   0,  -3, 1), (       1,        5) ),
    ( (1,  -3,   0,  -2,   0,  -3, 1), (       1,        5) ),
    ( (1,  -3,   0,  -3,   0,  -3, 1), (       1,        5) ),
    ( (1,  -3,   0,  -4,   0,  -3, 1), (       6,       23) ),
    ( (1,  -3,   1,   1,   1,  -3, 1), (       1,        8) ),
    ( (1,  -3,   1,  -1,   1,  -3, 1), (       1,        6) ),
    ( (1,  -3,   1,  -3,   1,  -3, 1), (       1,        6) ),
    ( (1,  -3,   1,  -5,   1,  -3, 1), (       1,       12) ),
    ( (1,  -3,   2,  -1,   2,  -3, 1), (       1,        8) ),
    ( (1,  -3,   2,  -2,   2,  -3, 1), (       1,        6) ),
    ( (1,  -3,   2,  -4,   2,  -3, 1), (       1,       10) ),
    ( (1,  -3,   2,  -5,   2,  -3, 1), (       1,       10) ),
    ( (1,  -3,   3,  -3,   3,  -3, 1), (       1,        6) ),
    ( (1,  -3,   3,  -5,   3,  -3, 1), (       1,       10) ),
    ( (1,  -4, -18, -27, -18,  -4, 1), (   19812,       21) ),
    ( (1,  -4, -17, -25, -17,  -4, 1), (       1,      125) ),
    ( (1,  -4, -16, -23, -16,  -4, 1), (       1,       39) ),
    ( (1,  -4, -16, -24, -16,  -4, 1), (      19,      632) ),
    ( (1,  -4, -15, -22, -15,  -4, 1), (    3635,       60) ),
    ( (1,  -4, -14, -19, -14,  -4, 1), (       1,       13) ),
    ( (1,  -4, -14, -21, -14,  -4, 1), (       1,       23) ),
    ( (1,  -4, -13, -17, -13,  -4, 1), (       1,       40) ),
    ( (1,  -4, -13, -18, -13,  -4, 1), (    1139,      182) ),
    ( (1,  -4, -12, -15, -12,  -4, 1), (    1377,       88) ),
    ( (1,  -4, -12, -16, -12,  -4, 1), (       1,       28) ),
    ( (1,  -4, -12, -17, -12,  -4, 1), (      28,       19) ),
    ( (1,  -4, -11, -13, -11,  -4, 1), (       1,       17) ),
    ( (1,  -4, -11, -14, -11,  -4, 1), (     101,       14) ),
    ( (1,  -4, -11, -15, -11,  -4, 1), (   55251,    10256) ),
    ( (1,  -4, -11, -16, -11,  -4, 1), (       1,       15) ),
    ( (1,  -4, -10, -11, -10,  -4, 1), (       1,       27) ),
    ( (1,  -4, -10, -12, -10,  -4, 1), (       1,       32) ),
    ( (1,  -4, -10, -13, -10,  -4, 1), (       6,       35) ),
    ( (1,  -4, -10, -14, -10,  -4, 1), (       1,       47) ),
    ( (1,  -4, -10, -15, -10,  -4, 1), (       1,       15) ),
    ( (1,  -4,  -9,  -9,  -9,  -4, 1), (       1,       35) ),
    ( (1,  -4,  -9, -10,  -9,  -4, 1), (       1,       11) ),
    ( (1,  -4,  -9, -11,  -9,  -4, 1), (       1,       11) ),
    ( (1,  -4,  -9, -12,  -9,  -4, 1), (       1,       11) ),
    ( (1,  -4,   0,   5,   0,  -4, 1), (       1,       12) ),
    ( (1,  -4,   0,   3,   0,  -4, 1), (       1,        8) ),
    ( (1,  -4,   0,   2,   0,  -4, 1), (       1,        8) ),
    ( (1,  -4,   0,   1,   0,  -4, 1), (       1,        8) ),
    ( (1,  -4,   0,   0,   0,  -4, 1), (       1,        5) ),
    ( (1,  -4,   0,  -1,   0,  -4, 1), (       1,        5) ),
    ( (1,  -4,   0,  -3,   0,  -4, 1), (       1,        5) ),
    ( (1,  -4,   0,  -4,   0,  -4, 1), (       1,        5) ),
    ( (1,  -4,   0,  -5,   0,  -4, 1), (       6,       35) ),
    ( (1,  -4,   0,  -7,   0,  -4, 1), (       1,       12) ),
    ( (1,  -4,   1,   3,   1,  -4, 1), (       1,       12) ),
    ( (1,  -4,   1,   2,   1,  -4, 1), (       1,        8) ),
    ( (1,  -4,   1,   1,   1,  -4, 1), (       1,        8) ),
    ( (1,  -4,   1,  -1,   1,  -4, 1), (       1,        6) ),
    ( (1,  -4,   1,  -2,   1,  -4, 1), (       1,        6) ),
    ( (1,  -5, -22, -33, -22,  -5, 1), ( 8604828,     9101) ),
    ( (1,  -5,  -2, -11,  -2,  -5, 1), (      -1,       -1) ),
    ( (1,  -6, -26, -39, -26,  -6, 1), (      -1,       -1) ),
    ( (1,  -6, -21, -31, -21,  -6, 1), (      -1,       -1) ),
    ( (1,  -6,  -5, -14,  -5,  -6, 1), (39420662, 93218808) ),
    ( (1,  -7, -29, -43, -29,  -7, 1), (      -1,       -1) ),
    ( (1,  -7, -28, -41, -28,  -7, 1), (      -1,       -1) ),
    ( (1,  -7, -13, -15, -13,  -7, 1), (  464594,    88425) ),
    ( (1,  -7,  -9, -15,  -9,  -7, 1), (   16784,     1319) ),
    ( (1,  -8, -33, -49, -33,  -8, 1), (      -1,       -1) ),
    ( (1,  -8, -30, -44, -30,  -8, 1), (      -1,       -1) ),
    ( (1,  -8, -26, -38, -26,  -8, 1), (      -1,       -1) ),
    ( (1,  -8, -24, -33, -24,  -8, 1), (   69544,     1623) ),
    ( (1,  -8, -23, -34, -23,  -8, 1), (      -1,       -1) ),
    ( (1,  -8, -19, -22, -19,  -8, 1), (   10715,      855) ),
    ( (1,  -8, -12, -17, -12,  -8, 1), (   18203,     3405) ),
    ( (1,  -8,  -9, -17,  -9,  -8, 1), (   25796,      424) ),
    ( (1,  -8,  -3, -17,  -3,  -8, 1), (      -1,       -1) ),
    ( (1,  -8,  11, -18,  11,  -8, 1), (   39493,     1229) ),
    ( (1,  -9, -37, -55, -37,  -9, 1), (  530787,      443) ),
    ( (1,  -9, -35, -51, -35,  -9, 1), (      -1,       -1) ),
    ( (1,  -9, -28, -41, -28,  -9, 1), (      -1,       -1) ),
    ( (1,  -9, -23, -28, -23,  -9, 1), ( 1979174,    11754) ),
    ( (1,  -9, -10, -19, -10,  -9, 1), (  102925,      421) ),
    ( (1,  -9,  -6, -20,  -6,  -9, 1), (      -1,       -1) ),
    ( (1, -10, -41, -61, -41, -10, 1), (      -1,       -1) ),
    ( (1, -10, -40, -59, -40, -10, 1), (      -1,       -1) ),
    ( (1, -10, -36, -52, -36, -10, 1), (      -1,       -1) ),
    ( (1, -10, -31, -45, -31, -10, 1), (  542819,     1291) ),
    ( (1, -10, -25, -32, -25, -10, 1), (  653506,    87061) ),
    ( (1, -10, -23, -26, -23, -10, 1), (   16230,       33) ),
    ( (1, -10, -11, -21, -11, -10, 1), (  317310,      457) ),
    ( (1, -10,  -4, -21,  -4, -10, 1), (      -1,       -1) )
]

class Number_Type (Enum):
    D = 0
    M = 1
    P = 2

number_sizes = [
    ("smallest",       9),
    ("smaller",       99),
    ("small",        999),
    ("medium",      9999),
    ("big",        99999),
    ("bigger",    999999),
    ("huge",     9999999),
    ("titanic", 99999999),
    ("extreme",       -1)
]

def _get_number_size(datum, number_type):
    if datum[1][0] == -1:
        return "unknown"
    for label, size in number_sizes:
        if size == -1:
            return label
        if number_type == Number_Type.D and size >= datum[1][0] + datum[1][1] :
            return label
        if number_type == Number_Type.M and size >= datum[1][0]:
            return label
        if number_type == Number_Type.P and size >= datum[1][1]:
            return label

boyd = [{
    "D_label": _get_number_size(datum, Number_Type.D),
    "p_label": _get_number_size(datum, Number_Type.P),
    "m_label": _get_number_size(datum, Number_Type.M),
    "m": datum[1][0] if datum[1][0] > 0 else None,
    "p": datum[1][1] if datum[1][1] > 0 else None,
    "poly": Polynomial(datum[0])
} for datum in _boyd]

def filter_by_size(data, label, size):
    return list(filter(lambda datum: datum[label] == size, data))