import unittest
from unittest.mock import patch
from pymatgen.io.vasp.inputs import Kpoints
import argparse
from vsh.scripts.kpoints import write_kpoints

class TestWriteKpoints(unittest.TestCase):

    def print_expected_and_result(self):
        args = argparse.Namespace(mesh_type="monkhorst", mesh=(4, 4, 4), input=None, output=None)
        expected_kpoints = Kpoints.monkhorst_automatic(kpts=(4, 4, 4))

        with patch('builtins.print') as mock_print, patch('pymatgen.io.vasp.inputs.Kpoints.write_file') as mock_write_file:
            result = write_kpoints(args)

            print(expected_kpoints)
            print(result)

    def test_write_kpoints_monkhorst(self):
        args = argparse.Namespace(mesh_type="monkhorst", mesh=(4, 4, 4), input=None, output=None)
        expected_kpoints = Kpoints.monkhorst_automatic(kpts=(4, 4, 4))

        with patch('builtins.print') as mock_print, patch('pymatgen.io.vasp.inputs.Kpoints.write_file') as mock_write_file:
            result = write_kpoints(args)
            
            self.assertEqual(result, expected_kpoints)
            mock_print.assert_not_called()
            mock_write_file.assert_not_called()

    def test_write_kpoints_gamma(self):
        args = argparse.Namespace(mesh_type="gamma", mesh=(4, 4, 4), input=None, output=None)
        expected_kpoints = Kpoints.gamma_automatic(kpts=(4, 4, 4))

        with patch('builtins.print') as mock_print, patch('pymatgen.io.vasp.inputs.Kpoints.write_file') as mock_write_file:
            result = write_kpoints(args)

            self.assertEqual(result, expected_kpoints)
            mock_print.assert_not_called()
            mock_write_file.assert_not_called()

    # def test_write_kpoints_automatic(self):
    #     args = argparse.Namespace(mesh_type="automatic", mesh=(4, 4, 4), input="structure.cif", output=None)
    #     expected_kpoints = Kpoints.automatic_density((4, 4, 4))

    #     with patch('builtins.print') as mock_print, patch('pymatgen.io.vasp.inputs.Kpoints.write_file') as mock_write_file:
    #         result = write_kpoints(args)

    #         self.assertEqual(result, expected_kpoints)
    #         mock_print.assert_not_called()
    #         mock_write_file.assert_not_called()

    def test_write_kpoints_no_output(self):
        args = argparse.Namespace(mesh_type="monkhorst", mesh=(4, 4, 4), input=None, output=None)
        expected_kpoints = Kpoints.monkhorst_automatic(kpts=(4, 4, 4))

        with patch('builtins.print') as mock_print, patch('pymatgen.io.vasp.inputs.Kpoints.write_file') as mock_write_file:
            result = write_kpoints(args)

            self.assertEqual(result, expected_kpoints)
            mock_print.assert_called_once_with(expected_kpoints)
            mock_write_file.assert_not_called()

    def test_write_kpoints_with_output(self):
        args = argparse.Namespace(mesh_type="monkhorst", mesh=(4, 4, 4), input=None, output="KPOINTS")
        expected_kpoints = Kpoints.monkhorst_automatic(kpts=(4, 4, 4))

        with patch('builtins.print') as mock_print, patch('pymatgen.io.vasp.inputs.Kpoints.write_file') as mock_write_file:
            result = write_kpoints(args)

            self.assertEqual(result, expected_kpoints)
            mock_print.assert_not_called()
            mock_write_file.assert_called_once_with('KPOINTS')

if __name__ == '__main__':
    unittest.main()