# pylint: disable=trailing-whitespace, missing-final-newline
from decimal import Decimal, InvalidOperation
from unittest.mock import patch
import pytest
from plugins.calc import CalcCommand
import pytest
from plugins.calc import CalcCommand

# @pytest.mark.parametrize("a, b, operation_name, expected_output", [
#     (Decimal('1'), Decimal('1'), 'add', 'Result: 1 add 1 = 2'),
#     # (Decimal('5'), Decimal('3'), 'subtract', 'Result: 5 subtract 3 = 2'),
#     # (Decimal('2'), Decimal('3'), 'multiply', 'Result: 2 multiply 3 = 6'),
#     # Additional test cases can be added here for 'divide' and edge cases
# ])
# def test_calc_command_operations(a, b, operation_name, expected_output):
#     with patch('builtins.print') as mocked_print:
#         calc_command_instance = CalcCommand()
#         calc_command_instance.run_calculations(a, b, operation_name)
#         mocked_print.assert_called_with(expected_output)
        
# # def test_calc_command_valid_operations(capsys, a, b, operation, expected_output):
# #     CalcCommand.run_calculations(a, b, operation)
# #     captured = capsys.readouterr()
# #     assert expected_output in captured.out

# # def test_calc_command_unknown_operation():
# #     with patch('logging.error') as mock_error:
# #         calc_command_instance = CalcCommand()
# #         CalcCommand.run_calculations(calc_command_instance,"unknown", "1", "1", )
# #         mock_error.assert_called_with("Unknown operation: unknown")

# def test_calc_command_invalid_number_input(capsys):
#     with patch('logging.error') as mock_error:
#         calc_command_instance = CalcCommand()
#         CalcCommand.run_calculations(calc_command_instance, "add", "a", "1")

#         captured = capsys.readouterr()
#         assert "Invalid number input: add or a is not a valid number." in captured.out
#         # mock_error.assert_called_with(f"Invalid number input: add or a is not a valid number.")

# def test_calc_command_division_by_zero(capsys):
#     with patch('logging.error') as mock_error:
#         calc_command_instance = CalcCommand()
#         CalcCommand.run_calculations("1", "0", "divide")
#         mock_error.assert_called_with("An error occurred: Cannot divide by zero.")

# def test_execute_with_valid_input(capsys):
#     command = CalcCommand()
#     command.execute("add","2", "3")
#     captured = capsys.readouterr()
#     assert "Result: 2 add 3 = 5" in captured.out

# def test_execute_with_incorrect_args(capsys):
#     with patch('logging.error') as mock_error:
#         command = CalcCommand()
#         command.execute("2")  # Insufficient arguments
#         mock_error.assert_called_with(f"Error: Missing arguments. Please follow Usage guide")
#         # assert "Error: Missing arguments. Please follow Usage guide" in captured.out

# def test_execute_integration(capsys):
#     command = CalcCommand()
#     command.execute("divide","10", "5")
#     captured = capsys.readouterr()
#     assert "Result: 10 divide 5 = 2" in captured.out