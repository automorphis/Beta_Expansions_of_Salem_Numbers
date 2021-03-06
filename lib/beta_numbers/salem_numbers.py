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
from mpmath import workdps, polyroots, im, re, almosteq

from beta_numbers.utilities import Int_Polynomial


class Salem_Number:
    """A class representing a Salem number.

    A minimal polynomial p over Z with the following properties uniquely characterizes a Salem number:
        * p is reciprocal and has even degree
        * p has two positive real roots, one of norm more than 1 and the other of norm less than 1
        * the non-real roots of p all have modulus exactly 1.
    """

    def __init__(self, min_poly, beta0 = None):
        """

        :param min_poly: Type `numpy.poly1d`. Should be checked to actually be the minimal polynomial of a Salem number
        before calling this method.
        :param dps: Guaranteed number of correct digits of `beta0` from the mathematically correct maximum modulus root of
        `min_poly`.
        :param beta0: Default `None`. Can also be calculated with a call to `calc_beta0`.
        """

        self.min_poly = min_poly
        self.dps = self.min_poly.get_dps()
        self.beta0 = beta0
        self.deg = self.min_poly.get_deg()
        self.conjs = None

    def __eq__(self, other):
        return self.min_poly == other.min_poly and self.dps == other.dps

    def __hash__(self):
        return hash(self.min_poly)

    def __str__(self):
        if self.beta0:
            return "(%.9f, %s)" % (self.beta0, self.min_poly)
        else:
            return str(self.min_poly)

    def __repr__(self):
        return "Salem_Number(%s)" % (repr(self.min_poly))

    def get_trace(self):
        return -self.min_poly[1]

    def calc_beta0(self, remember_conjs = False):
        """Calculates the maximum modulus root of `self.min_poly` to within `self.min_poly.get_dps()` digits bits of precision.

        :param remember_conjs: Default `False`. Set to `True` and access the conjugate roots via `self.conjs`. The number
        `self.conjs[0]` is the Salem number, `self.conjs[1]` is its reciprocal, and `self.conjs[2:]` have modulus 1.
        :raises: `NotSalemError`, if `self.min_poly` is not the minimal polynomial of a Salem number.
        :return: `beta0`, for convenience. Also sets `self.beta0` to the return value.
        """
        if self.deg < 4:
            raise Not_Salem_Error(self)
        if not self.beta0 or (remember_conjs and not self.conjs):
            with workdps(self.dps):
                rts = polyroots(list(map(int, list(self.min_poly.ndarray_coefs(False)))))
                if len(rts) < 4 or len(rts) % 2 == 1:
                    raise Not_Salem_Error(self)
                rts = sorted(rts, key=lambda z: abs(im(z)))
                self.beta0 = re(max(rts[:2], key=re))
                if remember_conjs:
                    beta0_recip = re(min(rts[:2], key=re))
                    self.conjs = [self.beta0, beta0_recip] + rts[2:]
        return self.beta0

    # def calc_beta0_global(self, remember_conjs = False):
    #     if not self.beta0 or (remember_conjs and not self.conjs):
    #         if self.min_poly == Polynomial((0,)):
    #             raise Not_Salem_Error(self)
    #         rts = polyroots( convert_polynomial_format(self.min_poly) )
    #         if len(rts) < 4 or len(rts) % 2 == 1:
    #             raise Not_Salem_Error(self)
    #         rts = sorted(rts, key=lambda z: abs(im(z)))
    #         self.beta0 = re(max(rts[:2], key=re))
    #         if remember_conjs:
    #             beta0_recip = re(min(rts[:2], key=re))
    #             self.conjs = [self.beta0, beta0_recip] + rts[2:]
    #     return self.beta0

    def check_salem(self):
        """Check that this object actually encodes a Salem number as promised. Raises `Not_Salem_Error` if not."""
        self.calc_beta0(True)
        with workdps(self.dps):
            if not(self.conjs[1] < 1 < self.conjs[0] and all(almosteq(abs(conj), 1) for conj in self.conjs[2:])):
                raise Not_Salem_Error(self)

    def change_dps(self,dps):
        return Salem_Number(self.min_poly,dps)

    def verify_calculated_beta0(self):
        if self.beta0:
            with workdps(self.dps):
                return almosteq(
                    self.min_poly.eval(self.beta0),
                    0
                )
        else:
            return None


def _is_salem_6poly(a, b, c, dps):
    U = Int_Polynomial([c - 2 * a, b - 3, a, 1], dps)
    if U.eval(2) >= 0 or U.eval(-2) >= 0:
        return False
    for n in range(-1, max(abs(a), abs(b - 3), abs(c - 2 * a))+2):
        if U.eval(n) == 0:
            return False
    if U.eval(-1) > 0 or U.eval(0) > 0 or U.eval(1) > 0:
        return True
    else:
        P = Int_Polynomial([1,a,b,c,b,a,1], dps)
        try:
            Salem_Number(P,dps).check_salem()
            return True
        except Not_Salem_Error:
            return False

def salem_iter(deg, min_trace, max_trace, dps):
    if deg != 6:
        raise NotImplementedError
    for a in range(-min_trace, -max_trace - 1, -1):
        b_max = 7 + (5 - a) * 4
        c_max = 8 + (5 - a) * 6
        for b in range(-b_max, b_max + 1):
            for c in range(-c_max, c_max + 1):
                if _is_salem_6poly(a, b, c, dps):
                    P = Int_Polynomial([1, a, b, c, b, a, 1], dps)
                    beta = Salem_Number(P, dps)
                    beta.calc_beta0()
                    yield beta

class Not_Salem_Error(RuntimeError):
    def __init__(self,beta):
        super().__init__("Not a Salem number. min_poly = %s" % beta.min_poly)

# class Salem_Iter:
#     """Iterates over a finite list of `Salem_Numbers` satisfying certain given parameters. Currently only implemented for
#     degree six Salem numbers.
#     """
#
#     def __init__(self, deg, max_trace, dps):
#         """
#
#         :param deg: The degree of all Salem numbers returned by this iterator. MUST BE 6.
#         :param max_trace: The maximum trace of all Salem numbers returned by this iterator.
#         :param dps: Guaranteed number of correct bits of `beta0` from the mathematically correct maximum modulus root of
#         `min_poly`.
#         """
#         if deg != 6:
#             raise NotImplementedError
#         self.deg = deg
#         self.max_trace = max_trace
#         self.dps = dps
#         self.betas = None
#         self.i = 0
#
#     def __iter__(self):
#         self.betas = []
#         for a in range(0, -self.max_trace-1,-1):
#             b_max = 7 + (5-a)*4
#             c_max = 8 + (5-a)*6
#             for b in range(-b_max,b_max+1):
#                 for c in range(-c_max,c_max+1):
#                     if _is_salem_6poly(a, b, c):
#                         P = poly1d((1,a,b,c,b,a,1))
#                         beta = Salem_Number(P, self.dps)
#                         beta.calc_beta0()
#                         self.betas.append(beta)
#         return self
#
#     def __next__(self):
#         if self.i >= len(self.betas):
#             raise StopIteration
#         ret = self.betas[self.i]
#         self.i += 1
#         return ret