# pylint: disable=unnecessary-dunder-call, invalid-name, line-too-long, trailing-whitespace, missing-final-newline
''' This module will test at the Calculations level to test historical storage
and retireval'''
from decimal import Decimal
import pytest
from plugins.calc.calculator.calculation import Calculation
from plugins.calc.calculator.calculations import Calculations
from plugins.calc.calculator.operations import add, subtract, multiply, divide


# pytest.fixture marks as a 'fixture'
# a setup mechanism used by pytest to initialize a test environment.
# This preps the Calculations class for testing env by clearing and running tests
@pytest.fixture
def setup_calculations():
    """Clear history ==> add test calculations"""
    # Clear any existing calculation history to ensure a clean state for each test.
    Calculations.clear_history()
    # Add sample calculations to the history to set up a known state for testing.
    # These calculations represent typical use cases and allow tests to verify that
    # the history functionality is working as expected.
    Calculations.add_to_history(Calculation(Decimal('20'), Decimal('5'), add))
    Calculations.add_to_history(Calculation(Decimal('20'), Decimal('5'), subtract))
    Calculations.add_to_history(Calculation(Decimal('20'), Decimal('4'), subtract))
    Calculations.add_to_history(Calculation(Decimal('20'), Decimal('5'), multiply))
    Calculations.add_to_history(Calculation(Decimal('20'), Decimal('5'), divide))


def test_add_to_history(setup_calculations):
    """Test adding a calculation to the history."""

    # single Calculation instance
    calc = Calculation(Decimal('2'), Decimal('2'), add)
    Calculations.add_to_history(calc)# Add to history

    # test + fail mesasge
    assert Calculations.get_latest_calc() == calc, "Failed to add the calculation to the history"

def test_get_latest_calc(setup_calculations):
    ''' Tests the latest calculation retrieved'''
    latest_calc =  Calculations.get_latest_calc()
    assert latest_calc.a == Decimal('20') and latest_calc.b == Decimal('5'), "Failed to retrieve correct latest calculation"

def test_get_latest_with_history(setup_calculations):
    """Test the return of latest calculation if history is empty"""
    # No history prep
    assert Calculations.get_history(), "Expected None for latest calculation with empty history"

def test_get_latest_with_empty_history(setup_calculations):
    """Test the return of latest calculation if history is empty"""
    # Prep history by erasing
    Calculations.clear_history()
    assert Calculations.get_latest_calc() is None, "Expected None for latest calculation with empty history"

def test_find_by_operation(setup_calculations):
    """Test searching calculations by requested operation"""
    # Search specifically for subtract
    add_operations = Calculations.find_by_operation("subtract")

    # Test for exactly 2 calculations based on fixture
    assert len(add_operations) == 2, "Did not find the correct number of calculations with add operation"

    # Search for multiply calcs
    multiply_operations = Calculations.find_by_operation("multiply")
    # Test for exactly 1 multiply calc based on fixture
    assert len(multiply_operations) == 1, "Did not find the correct number of calculations with multiply operation"
