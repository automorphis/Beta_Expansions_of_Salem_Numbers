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
import logging
import os
import sys
from pathlib import Path
import pickle as pkl

import numpy as np
from mpmath import mpf
from numpy import poly1d

from mpmath import workdps

# register = Pickle_Register.discover(Path.home() / "beta_expansions")

# with (Path.home() / "beta_expansions" / "register.pkl").open("rb") as fh:
#     register = Pickle_Register(Path.home() / "beta_expansions",pkl.load(fh))

# print(register.list_orbits_calculated())
from beta_numbers.calc_periods import calc_period
from beta_numbers.data import Pickle_Register
from beta_numbers.salem_numbers import Salem_Number
from beta_numbers.utilities import Int_Polynomial

start_n = 1000000000
max_n = 2 * 10 ** 9
max_restarts = 4
starting_dps = 64
save_period = 100000

data_root = Path.home() / "beta_expansions"
saves_directory = data_root / "D7PZfTzDhXxA9DWWYkKj"
register_filename = saves_directory / "register.pkl"

register = Pickle_Register.discover(saves_directory)
# with register_filename.open("rb") as fh:
#     register = Pickle_Register(saves_directory, pkl.load(fh))


beta = Salem_Number(Int_Polynomial((1,-10,-40,-59,-40,-10,1), starting_dps))
#
logging.basicConfig(filename ="logs/find_close_orbit.log", level = logging.INFO)
#
# try:
calc_period(
    beta,
    start_n,
    max_n,
    max_restarts,
    starting_dps,
    save_period,
    register
)
# except KeyboardInterrupt:
#     with register_filename.open("wb") as fh:
#         pkl.dump(register.get_dump_data(), fh)
#     try:
#         sys.exit(0)
#     except SystemExit:
#         os._exit(0)
#


# filename1 = Path("../output/several_smaller_orbits.txt")
# filename2 = Path("../test/several_smaller_orbits.txt")

# with filename.open("w") as fh:
#     fh.write("[\n")
#     for datum in filter_by_size(boyd, "D_label", "smaller"):
#         beta = Salem_Number(datum["poly"], 256)
#         beta0 = beta.calc_beta0()
#         _, Bs, cs = calc_period_ram_only(beta,400,1,256)
#         with workdps(256):
#             fh.write("\t" + str((tuple(beta.min_poly), beta0, list(Bs), list(cs), Bs.p, Bs.m)) + ",\n")
#     fh.write("]")

# data = []
#
# with filename1.open("r") as fh:
#     for line in fh.readlines():
#         if "poly1d" in line:
#             with workdps(256):
#                 data.append(eval(line)[0])
#
# with filename2.open("w") as fh:
#     for datum in data:
#         with workdps(256):
#             Bs = datum[2]
#             Bs = [Polynomial(np.flip(B.coef)) for B in Bs]
#             datum = (datum[0], datum[1], Bs, datum[3], datum[4], datum[5])
#             fh.write(str(datum) + ",\n")


# beta_nearly_hits_integer = Salem_Number(poly1d((1, -10, -40, -59, -40, -10, 1)), 32)
#
# found_orbit, Bs, cs = calc_period_ram_only(
#     beta_nearly_hits_integer,
#     10 ** 7,
#     4,
#     32
# )
#
# print("success")
#
# with open(filename, "w") as fh:
#     fh.write("[\n")
#     for c,B in zip(cs, Bs):
#         fh.write("\t(%d, %s),\n" % (c, repr(B)))
#     fh.write("]")
#
#
