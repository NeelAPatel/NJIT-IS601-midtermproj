# pylint: disable=trailing-whitespace, missing-final-newline
'''This module tests the menu command with prepared plugin lists'''
from unittest.mock import patch
from plugins.menu import MenuCommand

def test_menu_with_no_plugins(capsys):
    '''Tests Menu with no plugin'''
    with patch('os.listdir', return_value=[]):
        # Instantiate the MenuCommand
        command = MenuCommand()

        # Execute the command, which should print the menu
        command.execute()

        # Capture the output printed to stdout and stderr
        captured = capsys.readouterr()
        # Assert the expected output when no plugins are registered
        expected_output = "Plugins Menu: \n// end of plugins list\n"
        assert captured.out == expected_output, "Output should match expected menu format with no plugins listed"


def test_menu_with_one_mock_plugin(capsys, tmp_path):
    '''Tests Menu with one plugin'''
    # Create a temporary "tester" directory in the tmp_path
    (tmp_path / "mock_test_plugin").mkdir()

    # Use patch to mock os.path.abspath and os.path.join to return the path to the tmp_path
    # This simulates the plugins directory containing only the "tester" directory
    with patch('os.path.abspath', return_value=str(tmp_path)), \
         patch('os.path.join', return_value=str(tmp_path)):

        # Instantiate and execute the MenuCommand
        command = MenuCommand()
        command.execute()

        # Capture the output
        captured = capsys.readouterr()

        # Assert the expected output with "tester" plugin listed
        expected_output = "Plugins Menu: \nmock_test_plugin\n// end of plugins list\n"
        assert captured.out == expected_output, "Output should include the 'tester' plugin in the plugins list"

def test_menu_with_all_plugin_variations(capsys, tmp_path):
    '''Tests Menu with multiple plugin and variations'''
    # Create a temporary "tester" directory in the tmp_path
    (tmp_path / "mock_test_plugin").mkdir()
    (tmp_path / "__pycache__").touch()
    (tmp_path / "__init__.py").touch()
    (tmp_path / "valid_plugin").mkdir()

    with patch('os.path.abspath', return_value=str(tmp_path)), \
         patch('os.path.join', return_value=str(tmp_path)):

        # Instantiate and execute the MenuCommand
        command = MenuCommand()
        command.execute()

        # Capture the output
        captured = capsys.readouterr()

        # Assert the expected output with "tester" plugin listed
        assert "__pycache__" not in captured.out, "'__pycache__' should be ignored and not listed in the output"
        assert "__init__.py" not in captured.out, "'__init__.py' should be ignored and not listed in the output"
        assert "valid_plugin" in captured.out, "'valid_plugin' should be listed in the output"
        assert "Plugins Menu: " in captured.out and "// end of plugins list" in captured.out, "Output should include the menu header and footer"
