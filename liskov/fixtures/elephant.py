# -*- coding: utf8 -*-
import unittest

class Elephant(object):
    def __init__(self, color="grey"):
        self._color = color

    def color(self):
        return self._color

class RoyalElephant(Elephant):
    def __init__(self, color="grey"):
        self._color = "blue"


class ElephantTest(unittest.TestCase):
    def test_it_can_be_grey(self):
        expected = 'grey'
        elephant = self.new_elephant(expected)
        self.assertEqual(expected, elephant.color())

    def test_it_can_be_blue(self):
        expected = 'blue'
        elephant = self.new_elephant(expected)
        self.assertEqual(expected, elephant.color())

    def test_it_can_be_white(self):
        expected = 'white'
        elephant = self.new_elephant(expected)
        self.assertEqual(expected, elephant.color())

    def new_elephant(self, color):
        return Elephant(color)
