# pylint: disable=trailing-whitespace, missing-final-newline, too-many-arguments
''' Tests the main app program'''
# import logging
import os
# import sys
from unittest.mock import patch, MagicMock
import pandas as pd
import pytest

# Importing the App class from the app package. Note: This assumes that the app package is accessible in your PYTHONPATH.
from app import App
# from app.Colorizer import Colorizer
# from commands import Command, CommandHandler

@pytest.fixture
def app_instance():
    '''Fixture to provide an App instance with mocked environment'''
    with patch('app.App.setup_log'), patch('app.App.setup_env_vars') as mock_setup_env_vars:
        # Mock environment variables
        mock_env_vars = {'LOG_LEVEL': 'INFO', 'LOG_COLORED': 'FALSE'}
        mock_setup_env_vars.return_value = mock_env_vars
        app = App()
    return app

def test_setup_env_vars(app_instance):
    '''Test if setup_env_vars correctly reads and returns environment variables'''
    with patch.dict(os.environ, {'TEST_VAR': 'dummy_value'}, clear=True):
        env_vars = app_instance.setup_env_vars()
        assert env_vars['TEST_VAR'] == 'dummy_value'

def test_setup_log(app_instance):
    '''Test if setup_log correctly sets up logging based on environment variables'''
    with patch('app.os.makedirs'), patch('app.os.path.exists', return_value=False), \
         patch('app.logging.basicConfig') as mock_basic_config, patch('app.logging.getLogger') as mock_get_logger:
        
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        app_instance.setup_log()

        mock_basic_config.assert_called()
        mock_logger.setLevel.assert_called()

def test_fetch_plugins(app_instance):
    '''Test if fetch_plugins correctly discovers and imports plugins'''
    with patch('app.os.path.abspath', return_value='/fake/plugin/path'), \
         patch('app.pkgutil.iter_modules', return_value=iter([('loader', 'dummy_plugin', True)])), \
         patch('app.importlib.import_module') as mock_import_module:

        mock_plugin_module = MagicMock()
        mock_import_module.return_value = mock_plugin_module

        app_instance.fetch_plugins()

        mock_import_module.assert_called_with('dummy_plugin')

def test_manage_history_existing_file(app_instance):
    '''Tests managing history function when file exists'''
    with patch('app.os.path.exists', return_value=True), \
         patch('app.pd.read_csv', return_value=pd.DataFrame({'num1': [1], 'operand': ['+'], 'num2': [1], 'result': [2]})) as mock_read_csv, \
         patch('app.log.info') as mock_logger_info:
        #  patch('app.pd.DataFrame.to_csv') as mock_to_csv, \
        history_df = app_instance.manage_history()

        mock_read_csv.assert_called()

        # Assert that the DataFrame has the expected columns
        expected_columns = ['num1', 'operand', 'num2', 'result']
        assert list(history_df.columns) == expected_columns

        # Assert that logger.info was called with the expected message
        mock_logger_info.assert_called_with("Loaded existing history file")

def test_manage_history_no_existing_file(app_instance):
    '''Test if manage_history correctly handles the absence of a history file and creates a new one'''
    with patch('app.os.path.exists', return_value=False), patch('app.pd.DataFrame.to_csv') as mock_to_csv:
        history_df = app_instance.manage_history()

        assert 'num1' in history_df.columns
        mock_to_csv.assert_called()


def test_setup_log_with_config_file(app_instance):
    '''Test if setup_log configures logging using a config file when available'''
    with patch('app.os.path.exists', return_value=True), \
         patch('app.logging.config.fileConfig') as mock_file_config:
        app_instance.setup_log()
        mock_file_config.assert_called()


def test_fetch_plugins_import_error(app_instance, caplog):
    '''Test logging of an ImportError during plugin import in fetch_plugins method'''
    dummy_plugin_name = 'nonexistent_plugin'

    # Mock pkgutil.iter_modules to return a dummy plugin
    with patch('app.pkgutil.iter_modules', return_value=[(None, dummy_plugin_name, True)]):
        # Mock importlib.import_module to raise ImportError for the dummy plugin
        with patch('app.importlib.import_module', side_effect=ImportError('mock import error')):
            # Ensure the root logger and its handlers are mocked
            with patch('app.logging.getLogger') as mock_get_logger:
                mock_logger = MagicMock()
                mock_get_logger.return_value = mock_logger
                
                # Execute the method to test
                app_instance.fetch_plugins()

                # Verify that the expected error message was logged
                assert any(f"Error while importing plugin {dummy_plugin_name}" in message for message in caplog.messages)

def test_start_hello_command_output(app_instance, capsys):
    '''Test the start method with 'hello' command to check 'Hello, World!' output and ensure the loop can exit'''
    # Define a side effect function for the input mock
    def input_side_effect(*args, **kwargs):
        # First call returns 'hello', second call raises StopIteration to break the loop
        yield 'hello'
        # return

    with patch('builtins.input', side_effect=input_side_effect()), \
            patch.object(app_instance, 'manage_history', return_value=MagicMock()), \
            patch.object(app_instance.command_handler, 'execute_command') as mock_execute_command:
        
        # Set side effect to print 'Hello, World!' for 'hello' command and then raise an exception
        def execute_command_side_effect(command):
            if command == 'hello':
                print('Hello, World!')
            raise StopIteration  # Raise an exception to simulate breaking out of the loop

        mock_execute_command.side_effect = execute_command_side_effect

        # Use a try-except block to catch the StopIteration and prevent the test from failing due to this exception
        try:
            app_instance.start()
        except StopIteration:
            pass  # The exception is expected to break out of the loop

        # Capture the output and verify 'Hello, World!' was printed
        captured = capsys.readouterr()
        assert 'Hello, World!' in captured.out

        # Verify 'hello' command was processed
        mock_execute_command.assert_called_once_with('hello')
