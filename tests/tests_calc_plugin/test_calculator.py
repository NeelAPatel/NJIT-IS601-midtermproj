# pylint: disable=unnecessary-dunder-call, invalid-name, line-too-long, trailing-whitespace, missing-final-newline
""" This module tests at the main calculator level where users operate the program"""
from plugins.calc.calculator import Calculator

def test_addition():
    '''Test the addition calculation'''
    assert Calculator.add(2,2) == 4

def test_subtraction():
    '''Test the subtraction calculation'''
    assert Calculator.subtract(2,2) == 0

def test_divide():
    '''Test the divide calculation'''
    assert Calculator.divide(2,2) == 1

def test_multiply():
    '''Test the multiply calculation'''
    assert Calculator.multiply(2,2) == 4
