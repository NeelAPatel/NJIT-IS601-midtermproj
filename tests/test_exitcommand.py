# pylint: disable=trailing-whitespace, missing-final-newline
''' Tests exit plugin'''
import pytest

from plugins.exit import ExitCommand  # Adjust the import path as necessary

def test_exit_command():
    '''test exit command'''
    exit_command = ExitCommand()
    # Use pytest.raises to catch the SystemExit exception
    with pytest.raises(SystemExit) as exit_exception:
        exit_command.execute()

    # Optionally, you can also check the exit message or code
    assert str(exit_exception.value) == "Exiting..."
