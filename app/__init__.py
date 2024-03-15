import importlib #For plugin import
import pkgutil # for plugin import
import os, sys

import logging as log, logging.config 

from dotenv import load_dotenv

from app.Colorizer import Colorizer
from commands import CommandHandler, Command


class App: 
    def __init__(self):
        #Env Vars 
        load_dotenv()
        self.env_settings = self.setup_env_vars()

        #log
        self.setup_log()
        
        #program
        self.command_handler = CommandHandler()
    

    def setup_env_vars(self):
        return {key: value for key, value in os.environ.items()}
    
    def setup_log(self): 
        #Set up Loggging path
        os.makedirs('logs', exist_ok=True)
        path_rel_log_conf = 'logging.conf'
        path_abs_log_conf = os.path.abspath(path_rel_log_conf)

        #Get Log_Level
        log_level = self.env_settings.get('LOG_LEVEL', 'DEBUG').upper()
        # numeric_level = getattr(logging, log_level, None)
        # if not isinstance(numeric_level, int):
        #     raise ValueError(f'Invalid log level: {log_level}')
        # # Determine if colorization is needed
        # colorize = self.env_settings.get('LOG_COLORED', 'DEFAULT').upper() in ['COLOR', 'GREY']

        # root_logger = logging.getLogger()
        

        # # Use config file for logger, otherwise take the defaults
        # if os.path.exists(path_abs_log_conf): 
        #     logging.config.fileConfig(path_abs_log_conf, disable_existing_loggers=False)
        # else:
        #     # Fallback basic configuration
        #     log.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # # Apply ColoredFormatter to console handler
        # for handler in root_logger.handlers:
        #     if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
        #         # Apply ColoredFormatter only to the console handler
        #         handler.setFormatter(Colorizer(env_settings=self.env_settings))
        #     handler.setLevel(numeric_level)
        # print(log.getLogger().level)
        # logging.info("Logging configured.")

        numeric_level = getattr(logging, log_level, None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {log_level}')
        colorize = self.env_settings.get('LOG_COLORED', 'DEFAULT').upper() in ['COLOR', 'GREY']
    
        root_logger = logging.getLogger()
        # Use config file for logger, otherwise take the defaults
        if os.path.exists(path_abs_log_conf):
            logging.config.fileConfig(path_abs_log_conf, disable_existing_loggers=False)
        else:
            # Fallback basic configuration
            logging.basicConfig(level=numeric_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Explicitly set the log level on the root logger and all handlers
        root_logger.setLevel(numeric_level)
        for handler in root_logger.handlers:
            handler.setLevel(numeric_level)

            if colorize and isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
                # Apply ColoredFormatter only to the console handler
                handler.setFormatter(Colorizer(env_settings=self.env_settings))

        # # Use config file for logger, otherwise take the defaults
        # if os.path.exists(path_abs_log_conf):
        #     print("My log used")
        #     logging.config.fileConfig(path_abs_log_conf, disable_existing_loggers=False)
        # else:
        #     print("fallback log used")
        #     # Fallback basic configuration
        #     logging.basicConfig(level=numeric_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
        # # Apply ColoredFormatter to console handler if needed
        # if colorize:
        #     for handler in root_logger.handlers:
        #         if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
        #             # Apply ColoredFormatter only to the console handler
        #             handler.setFormatter(Colorizer(env_settings=self.env_settings))
        #         handler.setLevel(numeric_level)
        #         handler.setLevel(numeric_level)
    
        # #Explicitly set the log level on the root logger to respect the log_level from env_settings
        # root_logger.setLevel(numeric_level)



        # # Apply Colorizer based on LOG_COLORED setting
        # if colorize:
        #     for handler in log.getLogger().handlers:
        #         if isinstance(handler, log.StreamHandler):
        #             handler.setFormatter(Colorizer(env_settings=self.env_settings))

        log.info("log configured.")

    def fetch_plugins(self): 
        path_rel_plugins_folder = 'plugins/'
        path_abs_plugins_folder = os.path.abspath(path_rel_plugins_folder)
        #For each item, item's name, and pkgFlag in path's list...
        
        # Ensure the absolute path of the plugins directory is in the Python path
        if path_abs_plugins_folder not in sys.path:
            sys.path.append(path_abs_plugins_folder)

        log.debug(f'ABS Path for plugins: {path_abs_plugins_folder}')

        # Iterate over all packages in the plugins directory
        for _, plugin_name, is_pkg in pkgutil.iter_modules([path_abs_plugins_folder]):
            if is_pkg:  # Ensure it's a package
                try:
                    # Import the plugin package
                    plugin_module = importlib.import_module(plugin_name)
                    # Assume register_plugins is a method to handle the plugin
                    self.register_plugins(plugin_module, plugin_name)
                except ImportError as e:
                    log.info(f"Error while importing plugin {plugin_name}: {e}")
    
    def register_plugins(self, plugin_module, plugin_name):
        # for each item in folder, check if theres a subclass and register it as a command
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            try:
                if issubclass(item, (Command)):
                    self.command_handler.register_command(plugin_name, item())
                    log.info(f"Plugin Loaded: {plugin_name}")
            except TypeError:
                continue  # Ignore if not class

    
    def start(self): 
        #Load Plugins
            #plugins include menu, exit, hello
        self.fetch_plugins()
        #Start repl menu
        
        try: 
            while True:  # Check the exit event
                command_input = input(f'{Colorizer.GREEN}>>> {Colorizer.RESET}').strip()
                self.command_handler.execute_command(command_input)
        except KeyboardInterrupt: 
            log.warning("App interrupted via keyboard. Exiting gracefully.")
            sys.exit(0)
        finally: 
            log.error("App terminated.")