import unittest
import shutil
from unittest.mock import Mock

from bears.vhdl.VHDLLintBear import VHDLLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.testing.BearTestHelper import generate_skip_decorator


VHDLLintBearTest = verify_local_bear(VHDLLintBear,
                                     ('test',),
                                     ('\t',))


@generate_skip_decorator(VHDLLintBear)
class VHDLLintBearTest(unittest.TestCase):

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = Mock('perl', return_value=None)
            self.assertEqual(VHDLLintBear.check_prerequisites(),
                             'perl is not installed.')

            shutil.which = Mock('bakalint.pl', return_value=None)
            self.assertEqual(VHDLLintBear.check_prerequisites(),
                             'bakalint is missing. Download it from '
                             '<http://fpgalibre.sourceforge.net/ingles.html'
                             '#tp46> and put it into your PATH.')
        finally:
            shutil.which = _shutil_which
