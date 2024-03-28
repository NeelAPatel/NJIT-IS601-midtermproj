import importlib #For plugin import
import pkgutil # for plugin import
import os, sys

import logging as log, logging.config 

from dotenv import load_dotenv

from app.Colorizer import Colorizer
from commands import CommandHandler, Command
import numpy as np
import pandas as pd
import data_store

import readline

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
        # Fetches and returns environment variables to set into app instance var
        return {key: value for key, value in os.environ.items()}
    
    def setup_log(self): 
        # Sets up the logging system for the entire program

        #Set up Loggging path
        os.makedirs('logs', exist_ok=True)
        path_rel_log_conf = 'logging.conf'
        path_abs_log_conf = os.path.abspath(path_rel_log_conf)
        
        #From ENV - Get Log_Level and its numeric level
        log_level = self.env_settings.get('LOG_LEVEL', 'DEBUG').upper()
        numeric_level = getattr(logging, log_level, None)

        #From ENV - Get colorizer flags 
        colorize = self.env_settings.get('LOG_COLORED', 'DEFAULT').upper() in ['COLOR','COLORED','GREY']
    
        #Setting the logger system - if config file exists, use that, else defaults are provided
        root_logger = logging.getLogger()
        if os.path.exists(path_abs_log_conf):
            logging.config.fileConfig(path_abs_log_conf, disable_existing_loggers=False) # logger config file
        else:
            logging.basicConfig(level=numeric_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #Default logging config

        # Explicitly set the log level on the root logger and all handlers; stream and file andler
        root_logger.setLevel(numeric_level)
        for handler in root_logger.handlers:
            handler.setLevel(numeric_level)
            if colorize and isinstance(handler, logging.StreamHandler) and handler.stream == sys.stderr:
                # Apply ColoredFormatter only to the console handler
                handler.setFormatter(Colorizer(env_settings=self.env_settings))

        log.debug("Log ABS Path:"+path_abs_log_conf)
        log.info("Log sytem configured.")

    def fetch_plugins(self): 
        # Fetches installed plugins from plugins folder 

        #Path to Plugins folder
        path_rel_plugins_folder = 'plugins/'
        path_abs_plugins_folder = os.path.abspath(path_rel_plugins_folder)
        
        # Ensure the absolute path of the plugins directory is in the Python path
        if path_abs_plugins_folder not in sys.path:
            sys.path.append(path_abs_plugins_folder)
        log.debug("Plugins ABS Path:"+path_abs_plugins_folder)

        #For each item, item's name, and pkgFlag in path's list...
        # Iterate over all packages in the plugins directory
        for _, plugin_name, is_pkg in pkgutil.iter_modules([path_abs_plugins_folder]):
            if is_pkg:  # Ensure it's a package
                try:
                    # Import the plugin package --> register
                    plugin_module = importlib.import_module(plugin_name)
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
                    log.info(f"Plugin Registered: {plugin_name}")
            except TypeError:
                continue  # Ignore if not class

    def manage_history(self):
        #get name of file from env
        hist_file_name = self.env_settings.get('HIST_FILE_NAME', 'calc_history.csv')
        path_rel_hist_folder = self.env_settings.get('HIST_FILE_PATH', '/')
        path_abs_hist_folder = os.path.abspath(path_rel_hist_folder)
        path_abs_hist_file = os.path.join(path_abs_hist_folder, hist_file_name)
        data_store.hist_path = path_abs_hist_file
        log.debug("History File ABS Path:"+path_abs_hist_file)
        
        # history file needs to be created and/or retrieved from storage
        columns = ['num1', 'operand', 'num2', 'result']
        if os.path.exists(path_abs_hist_file):
            try:
                myDF = pd.read_csv(path_abs_hist_file)
    
                # Check if file has no columns
                if myDF.columns.empty:
                    raise pd.errors.EmptyDataError
    
                log.info("Loaded existing history file")
            except pd.errors.EmptyDataError:
                log.error("History File: The file exists but is empty, initializing with columns")
                myDF = pd.DataFrame(columns=columns)
                myDF.to_csv(path_abs_hist_file, index=False)
                log.info("History File: Columns added and saved to " + path_abs_hist_file)
        else:
            log.error("History File: Could not locate pre-existing file, making new file")
            myDF = pd.DataFrame(columns=columns)
            myDF.to_csv(path_abs_hist_file, index=False)
            log.info("History File: New history file created at " + path_abs_hist_file)
            
        
        return myDF            

    def start(self): 
        self.fetch_plugins()
        log.info("All plugins loaded!")

        #Start repl menu
        data_store.hist_df = self.manage_history()
        log.info("History file ready!")

        print()
        print("Welcome to the Calculator App")
        try: 
            while True:  # Check the exit event
                print("Type 'exit' to exit and end the program")
                command_input = input(f'{Colorizer.GREEN}>>> {Colorizer.RESET}').strip()
                self.command_handler.execute_command(command_input)
        except KeyboardInterrupt: 
            log.error("App interrupted via keyboard. Exiting gracefully.")
            sys.exit(0)
        finally: 
            log.info("App terminated gracefully")