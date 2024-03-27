# pylint: disable=unnecessary-dunder-call, invalid-name, line-too-long, trailing-whitespace, missing-final-newline

""" This module will test at the individual Calculation level """
from decimal import Decimal
from typing import Callable
import pytest
from plugins.calc.calculator.calculation import Calculation
from plugins.calc.calculator.operations import add, divide, subtract, multiply

#Turns each 'row' which is a tuple of elements into parameters
#testing different numbers/type combos to ensure correctedness
@pytest.mark.parametrize("a, b, operation, expected", [
    (Decimal('10'), Decimal('5'), add, Decimal('15')),
    (Decimal('10'), Decimal('5'), subtract, Decimal('5')),
    (Decimal('10'), Decimal('5'), multiply, Decimal('50')),
    (Decimal('10'), Decimal('2'), divide, Decimal('5')),
    (Decimal('10.5'), Decimal('0.5'), add, Decimal('11.0')),
    (Decimal('10.5'), Decimal('0.5'), subtract, Decimal('10.0')),
    (Decimal('10.5'), Decimal('2'), multiply, Decimal('21.0')),
    (Decimal('10'), Decimal('0.5'), divide, Decimal('20')),
])

def test_calc_perform(a: Decimal,b: Decimal, operation: Callable[[Decimal, Decimal], Decimal],
                      expected: Decimal):
    '''tests for the single calculation instance'''
    calc = Calculation(a, b, operation)
    #perform and ensure its as expected
    # comma , onwards = fail message
        # if failed, print out exactly what inputs were used and how it failed with which operation
        # operation.name prints out function name that was called
    assert calc.perform() == expected, f"Failed {operation.__name__} operation with {a} and {b}"

def test_calc_repr():
    '''tests the string representation output'''
    calc = Calculation(Decimal('5'), Decimal('10'), add)
    expected = "Calculation(5, 10, add)"
    #ensure fail message has been added
    assert calc.__repr__() == expected, '''The '__repr__' method failed to output the
     expected response.'''

def test_div_by_zero():
    '''testing the divide by zero functionality'''
    calc = Calculation(Decimal('5'), Decimal('0'), divide)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.perform()
