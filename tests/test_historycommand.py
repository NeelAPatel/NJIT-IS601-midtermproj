import pytest
from unittest.mock import MagicMock, patch
from plugins.history import HistoryCommand
import data_store
import pandas as pd

@pytest.fixture(params=['empty', 'with_data', 'default'])
def setup_history_df(request):
    # Initialize DataFrame with necessary columns in all cases
    columns = ['num1', 'operand', 'num2', 'result']
    if request.param == 'with_data':
        data_store.hist_df = pd.DataFrame({
            'num1': [1, 5],
            'operand': ['+', '*'],
            'num2': [1, 4],
            'result': [2, 20]
        })
    elif request.param == 'default':
        # For 'dummy' function test, start with an empty DataFrame but with defined columns
        data_store.hist_df = pd.DataFrame(columns=['num1', 'operand', 'num2', 'result'])
    else:
        # For truly empty DataFrame
        data_store.hist_df = pd.DataFrame(columns=columns)
    yield data_store.hist_df
    del data_store.hist_df

def test_default_response(capsys):
    history_command_instance = HistoryCommand()
    history_command_instance.execute()

    captured = capsys.readouterr()
    assert "Usage: \n  history <command> [parameters]" in captured.out

@pytest.mark.parametrize("setup_history_df", ['with_data'], indirect=True)
def test_show_command_with_data(capsys, setup_history_df):
    history_command_instance = HistoryCommand()
    history_command_instance.execute("show")

    captured = capsys.readouterr()
    assert captured.out.startswith("   num1 operand")

@pytest.mark.parametrize("setup_history_df", ['empty'], indirect=True)
def test_show_command_with_empty(capsys, setup_history_df):
    history_command_instance = HistoryCommand()
    history_command_instance.execute("show")

    captured = capsys.readouterr()
    assert "Empty DataFrame" in captured.out

@pytest.mark.parametrize("setup_history_df", ['empty'], indirect=True)
def test_last_function_empty_df(capsys, setup_history_df):
    with patch('plugins.history.log.error') as mock_log_error:
        history_command_instance = HistoryCommand()
        history_command_instance.last()

        mock_log_error.assert_called_once_with("Data frame is empty.")

@pytest.mark.parametrize("setup_history_df", ['with_data'], indirect=True)
def test_last_function_with_data(capsys, setup_history_df):
    history_command_instance = HistoryCommand()
    history_command_instance.last()

    captured = capsys.readouterr()
    assert captured.out.startswith("num1 ")


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_dummy_function(capsys, setup_history_df):
     with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error, \
            patch('plugins.history.log.info') as mock_log_info:
            # patch('plugins.history.log.debug') as mock_log_debug, \
        history_command_instance = HistoryCommand()
        history_command_instance.dummy()

        captured = capsys.readouterr()
        assert "New Dummy calculation added:" in captured.out
        assert "{'num1': 5, 'operand': '*', 'num2': 4, 'result': 20}" in captured.out


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_add_function(capsys, setup_history_df):
     with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error, \
            patch('plugins.history.log.info') as mock_log_info:

            # patch('plugins.history.log.debug') as mock_log_debug, \
        history_command_instance = HistoryCommand()

        # Execute the 'add' command with parameters '1 + 1 2'
        history_command_instance.execute('add', '1', '+', '1', '2')

        # Capture the output
        captured = capsys.readouterr()

        # Assert that log.debug was called with the expected parameters
        # mock_log_debug.assert_called_with(('add', '1', '+', '1', '2'))

        # Assert that the expected messages were printed
        expected_output = (
            "New calculation added: \n"
            "{'num1': '1', 'operand': '+', 'num2': '1', 'result': '2'}\n"
        )
        assert expected_output in captured.out

        # Additionally, you can assert that the DataFrame has been updated with the new calculation
        new_calculation = {'num1': '1', 'operand': '+', 'num2': '1', 'result': '2'}
        assert new_calculation.items() <= data_store.hist_df.iloc[-1].to_dict().items()
            
@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_add_function_too_many_args(capsys, setup_history_df):
     with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error, \
            patch('plugins.history.log.info') as mock_log_info:
            # patch('plugins.history.log.debug') as mock_log_debug, \ 
        history_command_instance = HistoryCommand()

        # Execute the 'add' command with too many parameters
        history_command_instance.execute('add', '1', '+', '1', '2', 'extra_arg')

        # Capture the output
        captured = capsys.readouterr()

        # Assert that log.error was called with the expected error message
        expected_error_msg = "Error: Incorrect arguments for 'history add': $> history add <num1> <sign> <num2> <result>"
        mock_log_error.assert_called_with(expected_error_msg)

        # Assert that the output includes the message about adding a new calculation
        assert "New calculation added:" not in captured.out

        # Optionally, assert that no new rows were added to the DataFrame
        assert len(data_store.hist_df) == 0  # Assumes DataFrame was initially empty


# @pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_add_function_incorrect_symbol(capsys, setup_history_df):
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error, \
            patch('plugins.history.log.info') as mock_log_info:

        history_command_instance = HistoryCommand()
        history_command_instance.execute('add', '1', '$', '1', '2')

        captured = capsys.readouterr()

        expected_error_msg = "Error: Invalid sign symbol for 'history add': sign= +, -, *, / "
        mock_log_error.assert_called_with(expected_error_msg)