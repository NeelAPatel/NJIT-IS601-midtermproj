import pytest
from unittest.mock import MagicMock, patch
from plugins.history import HistoryCommand
import data_store
import pandas as pd

# Single fixture for setting up DataFrame in different states
@pytest.fixture
def setup_history_df(request):
    if request.param == 'with_data':
        data_store.hist_df = pd.DataFrame({
            'num1': [1, 5],
            'operand': ['+', '*'],
            'num2': [1, 4],
            'result': [2, 20]
        })
    else:
        data_store.hist_df = pd.DataFrame(columns=['num1', 'operand', 'num2', 'result'])

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


