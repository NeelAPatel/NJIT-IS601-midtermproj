import os, sys

import logging, logging.config

from dotenv import load_dotenv

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
        
        # Apply ColoredFormatter based on LOG_COLORED setting
        if self.env_settings.get('LOG_COLORED', 'DEFAULT').upper() in ['COLOR', 'GREY']:
            for handler in logging.getLogger().handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setFormatter(ColoredFormatter(env_settings=self.env_settings))


        logging.error("Logging configured.")


    def start(self): 
        print("Hello, world");
        pass