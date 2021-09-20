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

import shutil
from pathlib import Path
from unittest import TestCase

import psutil
from numpy.polynomial.polynomial import Polynomial

from src.beta_orbit import calc_next_iterate, calc_period_ram_only, calc_period_ram_and_disk
from src.periodic_list import Periodic_List
from src.salem_numbers import Salem_Number
from src.save_states import Pickle_Register, Save_State_Type
from src.utility import eval_code_in_file, BYTES_PER_MB, BYTES_PER_KB, BYTES_PER_GB


class Test_Beta_Orbit_Iter(TestCase):
    pass

class Test_Beta_Orbit(TestCase):

    def setUp(self):
        self.several_smaller_orbits = eval_code_in_file("several_smaller_orbits.txt", 256)
        self.tmp_dir = Path.home() / "tmp_saves"
        self.beta_nearly_hits_integer = Salem_Number(Polynomial((1,-10,-40,-59,-40,-10,1)), 32)
        if Path.is_dir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def tearDown(self):
        if Path.is_dir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

    def test_calc_next_iterate(self):
        dps = 32
        for min_poly, _, Bs, cs, p, m in self.several_smaller_orbits:
            old_B = Polynomial((1,))
            beta = Salem_Number(min_poly,dps)
            for n, (correct_B, c) in enumerate(zip(Bs,cs)):
                calculated_B = calc_next_iterate(beta,old_B,c)
                self.assertEqual(correct_B, old_B, "min_poly: %s, iterate %d" % (min_poly, n+1))
                old_B = calculated_B

    def test_calc_period_ram_only(self):
        starting_dps = 32
        max_n = 300
        max_restarts = 1
        for min_poly, _, actual_Bs, actual_cs, p, m in self.several_smaller_orbits:
            beta = Salem_Number(min_poly,starting_dps)
            actual_Bs = Periodic_List(actual_Bs, p, m)
            actual_cs = Periodic_List(actual_cs, p, m)
            found_orbit, calc_Bs, calc_cs = calc_period_ram_only(beta,max_n,max_restarts,starting_dps)
            self.assertTrue(found_orbit)
            self.assertEqual(actual_Bs, calc_Bs)
            self.assertEqual(actual_cs, calc_cs)


    def test_calc_period_ram_and_disk(self):
        starting_dps = 32
        max_n = 400
        max_restarts = 1
        save_periods = [1, 2, 3, 5, 7, 10, 11, 100, 1000]
        check_memory_period = 10000
        needed_bytes = 1

        #ram version only
        for length in save_periods:
            register = Pickle_Register(
                self.tmp_dir / ("length-%d" % length)
            )
            for min_poly, _, actual_Bs, actual_cs, p, m in self.several_smaller_orbits[:10]:
                beta = Salem_Number(min_poly, starting_dps)
                actual_Bs = Periodic_List(actual_Bs, p, m)
                actual_cs = Periodic_List(actual_cs, p, m)
                calc_period_ram_and_disk(
                    beta,
                    max_n,
                    max_restarts,
                    starting_dps,
                    length,
                    check_memory_period,
                    needed_bytes,
                    register
                )

                calc_Bs = Periodic_List(
                    list(register.get_all(Save_State_Type.BS, beta)),
                    register.get_p(Save_State_Type.BS, beta),
                    register.get_m(Save_State_Type.BS, beta)
                )

                calc_cs = Periodic_List(
                    list(register.get_all(Save_State_Type.CS, beta)),
                    register.get_p(Save_State_Type.CS, beta),
                    register.get_m(Save_State_Type.CS, beta)
                )

                self.assertEqual(
                    calc_Bs,
                    actual_Bs
                )

                self.assertEqual(
                    calc_cs,
                    actual_cs
                )

        if Path.is_dir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)

        # disk version only
        check_memory_periods = [5, 10, 25, 100]
        needed_bytes = psutil.virtual_memory().available + BYTES_PER_GB

        for check_memory_period in check_memory_periods:
            for length in save_periods:
                register = Pickle_Register(
                    self.tmp_dir / ("length-%d" % length)
                )
                for min_poly, _, actual_Bs, actual_cs, p, m in self.several_smaller_orbits[:10]:
                    beta = Salem_Number(min_poly, starting_dps)
                    actual_Bs = Periodic_List(actual_Bs, p, m)
                    actual_cs = Periodic_List(actual_cs, p, m)
                    if check_memory_period < length:
                        with self.assertRaises(RuntimeError):
                            calc_period_ram_and_disk(
                                beta,
                                max_n,
                                max_restarts,
                                starting_dps,
                                length,
                                check_memory_period,
                                needed_bytes,
                                register
                            )

                    else:
                        calc_period_ram_and_disk(
                            beta,
                            max_n,
                            max_restarts,
                            starting_dps,
                            length,
                            check_memory_period,
                            needed_bytes,
                            register
                        )

                        calc_Bs = Periodic_List(
                            list(register.get_all(Save_State_Type.BS, beta)),
                            register.get_p(Save_State_Type.BS, beta),
                            register.get_m(Save_State_Type.BS, beta)
                        )

                        calc_cs = Periodic_List(
                            list(register.get_all(Save_State_Type.CS, beta)),
                            register.get_p(Save_State_Type.CS, beta),
                            register.get_m(Save_State_Type.CS, beta)
                        )

                        self.assertEqual(
                            calc_Bs,
                            actual_Bs
                        )

                        self.assertEqual(
                            calc_cs,
                            actual_cs
                        )
                shutil.rmtree(self.tmp_dir)

        # ram and disk version
        check_memory_periods = [5, 10, 25, 100]


        for check_memory_period in check_memory_periods:
            for length in save_periods:
                register = Pickle_Register(
                    self.tmp_dir / ("length-%d" % length)
                )
                for min_poly, _, actual_Bs, actual_cs, p, m in self.several_smaller_orbits[:10]:
                    beta = Salem_Number(min_poly, starting_dps)
                    actual_Bs = Periodic_List(actual_Bs, p, m)
                    actual_cs = Periodic_List(actual_cs, p, m)
                    if check_memory_period < length:
                        with self.assertRaises(RuntimeError):
                            calc_period_ram_and_disk(
                                beta,
                                max_n,
                                max_restarts,
                                starting_dps,
                                length,
                                check_memory_period,
                                needed_bytes,
                                register
                            )

                    else:
                        needed_bytes = psutil.virtual_memory().available - 2 * BYTES_PER_MB
                        calc_period_ram_and_disk(
                            beta,
                            max_n,
                            max_restarts,
                            starting_dps,
                            length,
                            check_memory_period,
                            needed_bytes,
                            register
                        )

                        calc_Bs = Periodic_List(
                            list(register.get_all(Save_State_Type.BS, beta)),
                            register.get_p(Save_State_Type.BS, beta),
                            register.get_m(Save_State_Type.BS, beta)
                        )

                        calc_cs = Periodic_List(
                            list(register.get_all(Save_State_Type.CS, beta)),
                            register.get_p(Save_State_Type.CS, beta),
                            register.get_m(Save_State_Type.CS, beta)
                        )

                        self.assertEqual(
                            calc_Bs,
                            actual_Bs
                        )

                        self.assertEqual(
                            calc_cs,
                            actual_cs
                        )
                shutil.rmtree(self.tmp_dir)




