from unittest.mock import MagicMock, patch
import pytest
from plugins.history import HistoryCommand
import data_store
import pandas as pd

# ==== FIXTURES =====
@pytest.fixture
def setup_mock_dummy_frame(): #Mock DF for when .dummy() is called
    # Create a mock for the DataFrame
    mock_df = MagicMock()
    # Mock the __str__ method to return a string representation of the DataFrame
    mock_df.__str__.return_value = (
        "   num1 operand  num2  result\n"
        "0     5       *     4      20\n"
    )

    # Use patch to replace the DataFrame in data_store with our mock
    with patch('data_store.hist_df', mock_df):
        yield mock_df

@pytest.fixture
def setup_mock_empty_frame(): #Mock DF for when function is called but DF is empty
    # Create a mock for the DataFrame
    mock_df = MagicMock()
    # Mock the __str__ method to return a string representation of the DataFrame
    mock_df.__str__.return_value = (
        "Empty DataFrame"
    )
    with patch('data_store.hist_df', mock_df):
        yield mock_df


# @pytest.fixture
# def mock_hist_df():
#     with patch('data_store.hist_df', new_callable=MagicMock) as mock_df:
#         # Configure mock to support DataFrame operations used in the `dummy` function
#         mock_df.loc = MagicMock()
#         mock_df.reset_index = MagicMock()
#         yield mock_df
    

def test_default_response(capsys): # Anytime when default response is shown
    history_command_instance = HistoryCommand()
    history_command_instance.execute()

    captured = capsys.readouterr()
    assert "Usage: \n  history <command> [parameters]" in captured.out

def test_show_command_with_data(capsys, setup_mock_dummy_frame): #Call .show --> Contains data
    history_command_instance = HistoryCommand()
    history_command_instance.execute("show")

    captured = capsys.readouterr()

    # Assert that the captured output matches the mocked DataFrame's string representation
    expected_output = (
        "   num1 operand  num2  result\n"
    )
    # assert captured.out == expected_output
    assert captured.out.startswith(expected_output)

def test_show_command_with_empty(capsys, setup_mock_empty_frame): #Call .show --> Empty DF
    history_command_instance = HistoryCommand()
    history_command_instance.execute("show")

    captured = capsys.readouterr()

    # Assert that the captured output matches the mocked DataFrame's string representation
    expected_output = (
        "Empty DataFrame\n"
    )
    assert captured.out.startswith(expected_output)


#works
def test_dummy_function(capsys, mock_hist_df): # Call .dummy --> results in row added to DF
    history_command_instance = HistoryCommand()
    history_command_instance.dummy()  # Assuming 'dummy' can be called directly

    # Capture the output
    captured = capsys.readouterr()

    # Assert that the expected messages were printed
    expected_messages = [
        "New Dummy calculation added:",
        "{'num1': 5, 'operand': '*', 'num2': 4, 'result': 20}"
    ]
    for message in expected_messages:
        assert message in captured.out

    # Assert that a new row was attempted to be added to the mock DataFrame
    assert mock_hist_df.loc.__setitem__.called


# WORKS TILL HERE ===================================
    
@pytest.fixture
def mock_hist_df():
    # Initialize a mock DataFrame with necessary methods
    mock_df = MagicMock()
    mock_df.loc = MagicMock()
    mock_df.reset_index = MagicMock()

    # Use patch.dict to temporarily add 'hist_df' to data_store's dictionary
    with patch.dict(data_store.__dict__, {'hist_df': mock_df}):
        yield mock_df


@pytest.fixture
def setup_history_df():
    # Start with an empty DataFrame for the 'DataFrame is empty' test case
    data_store.hist_df = pd.DataFrame(columns=['num1', 'operand', 'num2', 'result'])
    yield
    del data_store.hist_df  # Clean up after the test

@pytest.fixture
def setup_history_df_with_data():
    # Initialize DataFrame with some data
    data_store.hist_df = pd.DataFrame({
        'num1': [1, 5],
        'operand': ['+', '*'],
        'num2': [1, 4],
        'result': [2, 20]
    })
    yield data_store.hist_df
    del data_store.hist_df  # Clean up after the test


@patch('logging.error')  # Adjust the patch location according to your project structure
def test_last_function_empty_df(mock_log_error, setup_history_df): # Call .last when DF is empty 
    history_command_instance = HistoryCommand()
    history_command_instance.last()

    # Assert that logging.error was called with the expected message
    mock_log_error.assert_called_once_with("Data frame is empty.")

def test_last_function_with_data(capsys, setup_history_df_with_data):
    history_command_instance = HistoryCommand()
    history_command_instance.last()

    # Capture the output
    captured = capsys.readouterr()

    # Assert that the output starts with "num1 "
    assert captured.out.startswith("num1 ")

def test_execute_calls_save(mock_hist_df):
    with patch.object(HistoryCommand, 'save', autospec=True) as mock_save:
        history_command_instance = HistoryCommand()

        # Execute a command that should trigger the autosave feature
        # Replace 'dummy' with an appropriate command from your implementation
        history_command_instance.execute('dummy')

        # Assert that the 'save' method was called as a result of executing the command
        mock_save.assert_called_once()

        # If you need to check the arguments with which `save` was called, you can use:
        # mock_save.assert_called_once_with('dummy')


# MIssing: add 
# delete
# save
# clear