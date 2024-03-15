
import sys
from commands import Command

class ExitCommand(Command):
    def execute(self):
        sys.exit("Exiting...")
