# Define the ColoredFormatter class outside the App class
import logging


class Colorizer(logging.Formatter):
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

    # def format(self, record):
    #     log_fmt = self.FORMAT
    #     log_colored_setting = self.env_settings.get('LOG_COLORED', 'DEFAULT').upper()
    #     full_message_color = self.DIM_GREY if log_colored_setting in ['COLOR', 'COLORED'] else ""
    #     levelname_color = self.COLOR_MAP.get(record.levelno, self.RESET) if log_colored_setting in ['COLOR', 'COLORED'] else ""

    #     # Apply color only to the log level part, and grey to the rest of the message if applicable
    #     record.levelname = f"{levelname_color}{record.levelname}{full_message_color}"
    #     formatted_message = super().format(record)

    #     return f"{full_message_color}{formatted_message}{self.RESET}"


    def format(self, record):
        log_fmt = self.FORMAT
        log_colored_setting = self.env_settings.get('LOG_COLORED', 'DEFAULT').upper()

        # Apply color only if colored logging is enabled
        if log_colored_setting in ['COLOR', 'COLORED']:
            full_message_color = self.DIM_GREY
            levelname_color = self.COLOR_MAP.get(record.levelno, self.RESET)

            # Apply color to the log level part
            record.levelname = f"{levelname_color}{record.levelname}{full_message_color}"
            formatted_message = super().format(record)

            # Return the colored message with a reset at the end
            return f"{full_message_color}{formatted_message}{self.RESET}"
        else:
            # For non-colored logging, use the default formatting without colors
            return super().format(record)
