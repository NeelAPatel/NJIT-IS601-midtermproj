# pylint: disable=trailing-whitespace, missing-final-newline, too-many-arguments
''' Tests calcPlugin file'''

from decimal import Decimal
from unittest.mock import MagicMock, patch
import pytest
from plugins.calc import CalcCommand

@pytest.mark.parametrize("val_a, val_b, operation_name, expected_output", [
    (Decimal('1'), Decimal('1'), 'add', 'Result: 1 add 1 = 2'),
    (Decimal('5'), Decimal('3'), 'subtract', 'Result: 5 subtract 3 = 2'),
    (Decimal('2'), Decimal('3'), 'multiply', 'Result: 2 multiply 3 = 6'),
])

@patch('data_store.hist_df')
def test_run_calculations(mock_hist_df, capsys, val_a, val_b, operation_name, expected_output):
    ''' Tests valid run calculations'''

    # Configure the mock to avoid AttributeError
    mock_hist_df.loc = MagicMock()

    calc_command_instance = CalcCommand()
    calc_command_instance.run_calculations(val_a, val_b, operation_name)

    # Capture the output
    captured = capsys.readouterr()
    
    assert captured.out.startswith(expected_output)

def test_unknown_operation(capsys):
    ''' Tests unknown operation calculation run'''
    with patch('logging.error') as mock_log_error:
        calc_command_instance = CalcCommand()
        calc_command_instance.run_calculations(Decimal('1'), Decimal('1'), 'nonexistent_operation')

        # Assert that no output is printed
        captured = capsys.readouterr()
        assert captured.out == ''

        # Assert the log error was called
        mock_log_error.assert_called_with("Unknown operation: nonexistent_operation")

def test_invalid_decimal_input(capsys):
    ''' Tests bad decimal input calculation run'''
    with patch('logging.error') as mock_log_error:
        calc_command_instance = CalcCommand()
        # Providing a clearly invalid decimal input
        calc_command_instance.run_calculations('not_a_decimal', Decimal('1'), 'add')

        # Assert that no output is printed to stdout
        captured = capsys.readouterr()
        assert captured.out == ''

        # Using assert_called_once() here as we expect a single call with a message containing 'Invalid number input'
        mock_log_error.assert_called_once()
        args, _ = mock_log_error.call_args
        assert 'Invalid number input' in args[0]

def test_division_by_zero(capsys):
    ''' Tests div by zero calculation run'''
    with patch('logging.error') as mock_log_error:
        calc_command_instance = CalcCommand()
        # Setting up a division by zero scenario
        calc_command_instance.run_calculations(Decimal('1'), Decimal('0'), 'divide')

        # Assert that no output is printed to stdout
        captured = capsys.readouterr()
        assert captured.out == ''

        # Assert that logging.error was called
        mock_log_error.assert_called_with("An error occurred: Cannot divide by zero")

def test_default_message(capsys):
    ''' Tests defaultMessage()'''
    calc_command_instance = CalcCommand()
    calc_command_instance.defaultMessage()

    # Capture the output
    captured = capsys.readouterr()
    expected_output = (
        'Usage: \n'
        '    calc <operation> <num1> <num2 if needed>\n'
        '\n'
        'Operations: \n'
        '    add <num1> <num2>       adds two numbers (num1+num2)\n'
        '    subtract <num1> <num2>  subtract num2 from num1 (num1-num2)\n'
        '    multiply <num1> <num2>  multiplies two numbers (num1*num2)\n'
        '    divide <num1> <num2>    divide num1 by num2 (num1/num2)\n'
    )

    assert captured.out == expected_output

def test_execute_with_valid_arguments(capsys):
    ''' Tests Execute() w/ valid arguments'''
    calc_command_instance = CalcCommand()
    calc_command_instance.execute("add", 1, 2)

    captured = capsys.readouterr()
    assert "Result: 1 add 2 = 3" in captured.out


def test_execute_with_no_arguments(capsys):
    ''' Tests Execute() w/ no arguments'''
    calc_command_instance = CalcCommand()
    calc_command_instance.execute()

    captured = capsys.readouterr()
    expected_output = (
        'Usage: \n'
        '    calc <operation> <num1> <num2 if needed>\n'
        '\n'
        'Operations: \n'
        '    add <num1> <num2>       adds two numbers (num1+num2)\n'
        '    subtract <num1> <num2>  subtract num2 from num1 (num1-num2)\n'
        '    multiply <num1> <num2>  multiplies two numbers (num1*num2)\n'
        '    divide <num1> <num2>    divide num1 by num2 (num1/num2)\n'
    )
    assert captured.out == expected_output

def test_execute_with_missing_arguments(capsys):
    ''' Tests Execute() w/ missing arguments'''
    with patch('logging.error') as mock_log_error:
        calc_command_instance = CalcCommand()
        calc_command_instance.execute("add", 1)

        # Assert that no output is printed
        captured = capsys.readouterr()
        assert captured.out == ''

        # Assert the log error was called with the expected message
        mock_log_error.assert_called_with("Error: Incorrect number of arguments for calc")
