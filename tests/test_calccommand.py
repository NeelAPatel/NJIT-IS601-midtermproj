'''This module tests the calc plugin'''
from decimal import InvalidOperation
from unittest.mock import patch
import pytest
from plugins.calc import CalcCommand

@pytest.mark.parametrize("val_a, val_b, operation, expected_result", [
    ("1", "1", "add", "Result: 1 add 1 = 2"),
    ("2", "1", "subtract", "Result: 2 subtract 1 = 1"),
    ("2", "3", "multiply", "Result: 2 multiply 3 = 6"),
    ("4", "2", "divide", "Result: 4 divide 2 = 2"),
])

def test_calc_command_valid_operations(capsys, val_a, val_b, operation, expected_result):
    '''Tests if a generic calculation has a valid operation'''
    CalcCommand.run_calculations(val_a, val_b, operation)
    captured = capsys.readouterr()
    assert expected_result in captured.out

def test_calc_command_unknown_operation():
    ''' Test for incorrect operation '''
    with patch('logging.error') as mock_error:
        CalcCommand.run_calculations("1", "1", "unknown")
        mock_error.assert_called_with("Unknown operation: unknown")

def test_calc_command_invalid_number_input(capsys):
    ''' Non number input'''
    with patch('logging.error') as mock_error:
        CalcCommand.run_calculations("a", "1", "add")
        mock_error.assert_called_with(f"Invalid number input: a or 1 is not a valid number: {InvalidOperation}")

def test_calc_command_division_by_zero(capsys):
    ''' Divide by zero'''
    with patch('logging.error') as mock_error:
        CalcCommand.run_calculations("1", "0", "divide")
        mock_error.assert_called_with("An error occurred: Cannot divide by zero.")

def test_execute_with_valid_input(capsys):
    ''' tests Execute command with valid input'''
    command = CalcCommand()
    command.execute("2", "3", "add")
    captured = capsys.readouterr()
    assert "Result: 2 add 3 = 5" in captured.out

def test_execute_with_incorrect_args(capsys):
    ''' tests Execute command with bad args'''
    command = CalcCommand()
    command.execute("2")  # Insufficient arguments
    captured = capsys.readouterr()
    assert "Usage: calc <number1> <number2> <operation>" in captured.out


def test_execute_integration(capsys):
    ''' tests Execute command'''
    command = CalcCommand()
    command.execute("10", "5", "divide")
    captured = capsys.readouterr()
    assert "Result: 10 divide 5 = 2" in captured.out
