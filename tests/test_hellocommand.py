# pylint: disable=trailing-whitespace, missing-final-newline
'''Tests Hello command'''
from plugins.hello import HelloCommand

def test_my_hello_command(capsys):
    ''' Tests for Hello Command '''
    # Execute the command which is expected to print "Hello, World!"
    HelloCommand().execute()

    # Capture the output
    captured = capsys.readouterr()

    # Assert that the captured output is as expected
    assert captured.out == "Hello, World!\n"
