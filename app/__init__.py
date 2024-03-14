import os, sys

import logging, logging.config

from dotenv import load_dotenv

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
        
        logging.info("Logging configured.")


    def start(self): 
        print("Hello, world");
        pass