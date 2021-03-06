# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

from __future__ import unicode_literals

import unittest2 as unittest

import os

from pymatgen.io.feff.sets import MPXANESSet
from pymatgen.io.feff.inputs import Potential
from pymatgen.io.cif import CifParser

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                        'test_files')


class FeffInputSetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.header_string = """* This FEFF.inp file generated by pymatgen
TITLE comment: From cif file
TITLE Source:  CoO19128.cif
TITLE Structure Summary:  Co2 O2
TITLE Reduced formula:  CoO
TITLE space group: (P6_3mc), space number:  (186)
TITLE abc:  3.297078   3.297078   5.254213
TITLE angles: 90.000000  90.000000 120.000000
TITLE sites: 4
* 1 Co     0.666667     0.333333     0.003676
* 2 Co     0.333334     0.666666     0.503676
* 3 O     0.333334     0.666666     0.121324
* 4 O     0.666667     0.333333     0.621325"""
        cif_file = os.path.join(test_dir, 'CoO19128.cif')
        cls.structure = CifParser(cif_file).get_structures()[0]
        cls.absorbing_atom = 'O'
        cls.mp_xanes = MPXANESSet(cls.absorbing_atom, cls.structure)

    def test_get_header(self):
        comment = 'From cif file'
        header = str(self.mp_xanes.header(source='CoO19128.cif', comment=comment))
        ref = self.header_string.splitlines()
        last4 = [" ".join(l.split()[2:]) for l in ref[-4:]]
        for i, l in enumerate(header.splitlines()):
            if i < 9:
                self.assertEqual(l, ref[i])
            else:
                s = " ".join(l.split()[2:])
                self.assertIn(s, last4)

    def test_getfefftags(self):
        tags = self.mp_xanes.tags.as_dict()
        self.assertEqual(tags['COREHOLE'], "FSR",
                         "Failed to generate PARAMETERS string")

    def test_get_feffPot(self):
        POT = str(self.mp_xanes.potential)
        d, dr = Potential.pot_dict_from_string(POT)
        self.assertEqual(d['Co'], 1, "Wrong symbols read in for Potential")

    def test_get_feff_atoms(self):
        atoms = str(self.mp_xanes.atoms)
        self.assertEqual(atoms.splitlines()[3].split()[4], self.absorbing_atom,
                         "failed to create ATOMS string")

    def test_to_and_from_dict(self):
        f1_dict = self.mp_xanes.as_dict()
        f2 = self.mp_xanes.from_dict(f1_dict)
        self.assertEqual(f1_dict, f2.as_dict())

    def test_user_tag_settings(self):
        tags_dict_ans = self.mp_xanes.tags.as_dict()
        tags_dict_ans["COREHOLE"] = "RPA"
        tags_dict_ans["EDGE"] = "L1"
        user_tag_settings = {"COREHOLE": "RPA", "EDGE": "L1"}
        mp_xanes_2 = MPXANESSet(self.absorbing_atom, self.structure,
                                user_tag_settings=user_tag_settings)
        self.assertEqual(mp_xanes_2.tags.as_dict(), tags_dict_ans)
        print(mp_xanes_2.as_dict().keys())


if __name__ == '__main__':
    unittest.main()
