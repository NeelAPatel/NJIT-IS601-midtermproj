import importlib #For plugin import
import pkgutil # for plugin import
import os, sys

import logging, logging.config

from dotenv import load_dotenv

from commands import CommandHandler, Command

# Define the ColoredFormatter class outside the App class
class ColoredFormatter(logging.Formatter):
    DIM_GREY = "\033[2;37m"  # Updated dim grey color code
    RED = "\033[31m"  # Non-bold red
    GREEN = "\033[32m"  # Non-bold green
    YELLOW = "\033[33m"  # Non-bold yellow
    BLUE = "\033[34m"  # Non-bold blue
    MAGENTA = "\033[35m"  # Non-bold magenta
    WHITE = "\033[37m"  # Non-bold white
    RESET = "\033[0m"
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    COLOR_MAP = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA,
    }

    def __init__(self, env_settings):
        super().__init__(self.FORMAT)
        self.env_settings = env_settings

    def format(self, record):
        log_fmt = self.FORMAT
        log_colored_setting = self.env_settings.get('LOG_COLORED', 'DEFAULT').upper()
        full_message_color = self.DIM_GREY if log_colored_setting in ['COLOR', 'COLORED'] else ""
        levelname_color = self.COLOR_MAP.get(record.levelno, self.RESET) if log_colored_setting in ['COLOR', 'COLORED'] else ""

        # Apply color only to the log level part, and grey to the rest of the message if applicable
        record.levelname = f"{levelname_color}{record.levelname}{self.RESET}"
        formatted_message = super().format(record)

        return f"{full_message_color}{formatted_message}{self.RESET}"


class App: 
    def __init__(self):
        #Env Vars 
        load_dotenv()
        self.env_settings = self.setup_env_vars()

        #Logging
        self.setup_logging()

        #program
        self.command_handler = CommandHandler()
    

    def setup_env_vars(self):
        return {key: value for key, value in os.environ.items()}
    
    def setup_logging(self): 
        os.makedirs('logs', exist_ok=True)
        path_rel_logging_conf = 'logging.conf'
        path_abs_logging_conf = os.path.abspath(path_rel_logging_conf)

        if os.path.exists(path_abs_logging_conf): 
            logging.config.fileConfig(path_abs_logging_conf, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # # Apply ColoredFormatter based on LOG_COLORED setting
        # if self.env_settings.get('LOG_COLORED', 'DEFAULT').upper() in ['COLOR', 'GREY']:
        #     for handler in logging.getLogger().handlers:
        #         if isinstance(handler, logging.StreamHandler):
        #             handler.setFormatter(ColoredFormatter(env_settings=self.env_settings))

        logging.error("Logging configured.")

    def fetch_plugins(self): 
        plugins_namespace = 'plugins'
        path_rel_plugins_folder = 'plugins/'
        path_abs_plugins_folder = os.path.abspath(path_rel_plugins_folder)
        #For each item, item's name, and pkgFlag in path's list...
        print(path_rel_plugins_folder)
        
        # Ensure the absolute path of the plugins directory is in the Python path
        if path_abs_plugins_folder not in sys.path:
            sys.path.append(path_abs_plugins_folder)

        # Iterate over all packages in the plugins directory
        for _, plugin_name, is_pkg in pkgutil.iter_modules([path_abs_plugins_folder]):
            if is_pkg:  # Ensure it's a package
                try:
                    # Import the plugin package
                    plugin_module = importlib.import_module(plugin_name)
                    # Assume register_plugins is a method to handle the plugin
                    self.register_plugins(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error while importing plugin {plugin_name}: {e}")
    
    def register_plugins(self, plugin_module, plugin_name):
        # for each item in folder, check if theres a subclass and register it as a command
        for item_name in dir(plugin_module):
            item = getattr(plugin_module, item_name)
            try:
                if issubclass(item, (Command)):
                    self.command_handler.register_command(plugin_name, item())
                    logging.info(f"Plugin Loaded: {plugin_name}")
            except TypeError:
                continue  # Ignore if not class

    
    def start(self): 
        #Load Plugins
            #plugins include menu, exit, hello
        self.fetch_plugins()
        #Start repl menu

        try: 
            while True:  # Check the exit event
                command_input = input(">>> ").strip()
                self.command_handler.execute_command(command_input)
        except KeyboardInterrupt: 
            logging.info("App interrupted via keyboard. Exiting gracefully.")
            sys.exit(0)
        finally: 
            logging.info("App terminated.")