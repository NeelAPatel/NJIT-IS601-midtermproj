# pylint: disable=trailing-whitespace, missing-final-newline, unused-variable
''' Tests the history plugin'''

from unittest.mock import patch
import pandas as pd
import pytest
from plugins.history import HistoryCommand
import data_store

@pytest.fixture(params=['empty', 'with_data', 'default'])
def setup_history_df(request):
    '''Fixture for history_df'''
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
    ''' Tests output fordefault response'''
    history_command_instance = HistoryCommand()
    history_command_instance.execute()

    captured = capsys.readouterr()
    assert "Usage: \n  history <command> [parameters]" in captured.out

@pytest.mark.parametrize("setup_history_df", ['with_data'], indirect=True)
def test_show_command_with_data(capsys, setup_history_df):
    ''' Tests output for show() function'''
    history_command_instance = HistoryCommand()
    history_command_instance.execute("show")

    captured = capsys.readouterr()
    assert captured.out.startswith("   num1 operand")

@pytest.mark.parametrize("setup_history_df", ['empty'], indirect=True)
def test_show_command_with_empty(capsys, setup_history_df):
    ''' Tests output for show() when df is empty'''
    history_command_instance = HistoryCommand()
    history_command_instance.execute("show")

    captured = capsys.readouterr()
    assert "Empty DataFrame" in captured.out


@pytest.mark.parametrize("setup_history_df", ['with_data'], indirect=True)
def test_last_function_with_data(capsys, setup_history_df):
    ''' Tests output for last() when data exists'''
    history_command_instance = HistoryCommand()
    history_command_instance.last()

    captured = capsys.readouterr()
    assert captured.out.startswith("num1 ")


@pytest.mark.parametrize("setup_history_df", ['empty'], indirect=True)
def test_last_function_empty_df(capsys, setup_history_df):
    ''' Tests output for last() when data doesnt exist'''
    with patch('plugins.history.log.error') as mock_log_error:
        history_command_instance = HistoryCommand()
        history_command_instance.last()

        mock_log_error.assert_called_once_with("Data frame is empty.")


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_dummy_function(capsys, setup_history_df):
    ''' Tests output for dummy() to load a dummy row of data'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'):
            # patch('plugins.history.log.debug') as mock_log_debug, \
        history_command_instance = HistoryCommand()
        history_command_instance.dummy()

        captured = capsys.readouterr()
        assert "New Dummy calculation added:" in captured.out
        assert "{'num1': 5, 'operand': '*', 'num2': 4, 'result': 20}" in captured.out


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_add_function(capsys, setup_history_df):
    ''' Tests output for add() to add custom row to data'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'):

            # patch('plugins.history.log.debug') as mock_log_debug, \
        history_command_instance = HistoryCommand()

        # Execute the 'add' command with parameters '1 + 1 2'
        history_command_instance.execute('add', '1', '+', '1', '2')

        # Capture the output
        captured = capsys.readouterr()

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
    ''' Tests output for add() with too many args'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error:
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
    ''' Tests output for add() but incorrect symbol was used'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error:

        history_command_instance = HistoryCommand()
        history_command_instance.execute('add', '1', '$', '1', '2')

        expected_error_msg = "Error: Invalid sign symbol for 'history add': sign= +, -, *, / "
        mock_log_error.assert_called_with(expected_error_msg)


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_delete_function(capsys, setup_history_df):
    ''' Tests output for delete() to delete a row'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'):

        history_command_instance = HistoryCommand()
        history_command_instance.execute('dummy')
        history_command_instance.execute('delete', '0')

         # Capture the output
        captured = capsys.readouterr()

        # Assert that the expected messages were printed
        expected_output = (
            "Row 0 deleted successfully."
        )
        assert expected_output in captured.out


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_delete_function_too_many_args(capsys, setup_history_df):
    ''' Tests output for delete() with too many args'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error:

        history_command_instance = HistoryCommand()
        history_command_instance.execute('dummy')
        history_command_instance.execute('delete', '0', '1')



        expected_error_msg = "Error: Incorrect number of arguments for 'delete'. Usage history delete [row_num]"
        mock_log_error.assert_called_with(expected_error_msg)


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_delete_function_index_not_int(capsys, setup_history_df):
    ''' Tests output for delete() but not integer'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error:

        history_command_instance = HistoryCommand()
        history_command_instance.execute('dummy')
        history_command_instance.execute('delete', 'abcd')



        expected_error_msg = "Error: Provided index is not an integer."
        mock_log_error.assert_called_with(expected_error_msg)



@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_delete_function_index_not_found(capsys, setup_history_df):
    ''' Tests output for delete() when row index is not found'''
    with patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.error') as mock_log_error:

        history_command_instance = HistoryCommand()
        history_command_instance.execute('dummy')
        history_command_instance.execute('delete', '9999999')

        expected_error_msg = "Error: No row found at index 9999999."
        mock_log_error.assert_called_with(expected_error_msg)

@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_delete_function_empty_table(capsys, setup_history_df):
    ''' Tests output for delete() when table is empty'''
    with patch('data_store.hist_path', 'dummy_path.csv'), \
         patch('plugins.history.log.error') as mock_log_error:

        history_command_instance = HistoryCommand()
        # Removed execute('dummy') to ensure the DataFrame remains empty
        history_command_instance.execute('delete', '0')  # Attempt to delete from an empty DataFrame

        expected_error_msg = "Error: Table is empty, no rows to delete."
        mock_log_error.assert_called_with(expected_error_msg)


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_reloadfile_file_exists(capsys, setup_history_df):
    ''' Tests output for reload() from csv file'''
    with patch('plugins.history.os.path.exists', return_value=True), \
         patch('plugins.history.pd.read_csv') as mock_read_csv, \
         patch('plugins.history.log.info') as mock_log_info:
        
        mock_read_csv.return_value = pd.DataFrame({'num1': [1], 'operand': ['+'], 'num2': [1], 'result': [2]})
        
        history_command_instance = HistoryCommand()
        history_command_instance.reloadfile()
        
        mock_log_info.assert_any_call("File read successfully")
        mock_log_info.assert_any_call("File reloaded")
        
        captured = capsys.readouterr()
        assert "Data successfully reloaded from file." in captured.out


@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_reloadfile_file_not_exists(capsys, setup_history_df):
    ''' Tests output for reload() when file doesnt exist'''
    with patch('plugins.history.os.path.exists', return_value=False), \
         patch('plugins.history.log.error') as mock_log_error:
        
        history_command_instance = HistoryCommand()
        history_command_instance.reloadfile()
        
        expected_error_msg = f"File not found at {data_store.hist_path}. Ensure the file path is correct."
        mock_log_error.assert_called_with(expected_error_msg)



@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_reloadfile_file_empty(capsys, setup_history_df):
    ''' Tests output for reload() when file is empty'''
    with patch('plugins.history.os.path.exists', return_value=True), \
         patch('plugins.history.pd.read_csv', side_effect=pd.errors.EmptyDataError), \
         patch('plugins.history.data_store.hist_path', 'dummy_path.csv'), \
         patch('plugins.history.log.error') as mock_log_error:

        history_command_instance = HistoryCommand()
        history_command_instance.reloadfile()

        # Assert that the expected error message was logged
        expected_error_msg = "File is empty. Starting with an empty DataFrame."
        mock_log_error.assert_called_with(expected_error_msg)

@pytest.mark.parametrize("setup_history_df", ['default'], indirect=True)
def test_clear_function(capsys, setup_history_df):
    ''' Tests output for clear()'''
    with   patch('plugins.history.os.path.exists', return_value=True), \
            patch('plugins.history.HistoryCommand.save') as mock_save, \
            patch('data_store.hist_path', 'dummy_path.csv'), \
            patch('plugins.history.log.info') as mock_log_info:

        history_command_instance = HistoryCommand()
        history_command_instance.execute('dummy')
        history_command_instance.execute('clear')

        expected_msg = "History - Dataframe cleared"
        mock_log_info.assert_called_with(expected_msg)
