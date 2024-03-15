

import os
from commands import Command


class MenuCommand(Command): 
    def execute(self): 

        print("Plugins Menu: ")
        commands_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plugins', '..', '..', ))
        # print (commands_path)
        folderIgnore = ['__pycache__', '__init__.py']
        for item in os.listdir(commands_path):
            # ignore pycache and other extraneous folders
            if item in folderIgnore: 
                continue
            print(item)
        print('// end of plugins list')