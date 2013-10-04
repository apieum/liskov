# -*- coding: utf8 -*-
import unittest
from liskov import *
import os.path
__dir__ = os.path.dirname(os.path.abspath(__file__))
append_sys_path(os.path.join(__dir__, 'fixtures'))

class LiskovSubstitutionTest(unittest.TestCase):

    def test_can_substitute_decorator_create_new_subtype(self):
        @can_substitute('calc.BasicCalc', 'convert.BasesConvert')
        class ScientificCalc(object):
            pass

        from calc import BasicCalc
        from convert import BasesConvert
        assert issubclass(ScientificCalc, (BasicCalc, BasesConvert))


    def test_substitute_metaclass_create_new_subtype(self):
        class ScientificCalc(object):
            __metaclass__ = behave_as('calc.BasicCalc', 'convert.BasesConvert')

        from calc import BasicCalc
        from convert import BasesConvert
        assert issubclass(ScientificCalc, (BasicCalc, BasesConvert))


    def test_subtypeof_import_a_class_in_nested_scope(self):
        class ScientificCalc(subtypeof('calc.BasicCalc')):
            pass

        from calc import BasicCalc
        assert issubclass(ScientificCalc, BasicCalc)
