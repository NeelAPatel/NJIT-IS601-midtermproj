from decimal import Decimal, InvalidOperation
import os
import sys

import pandas as pd

from commands import Command

from decimal import Decimal, InvalidOperation

from plugins.calc.calculator import Calculator
import logging as log

class CalcCommand(Command): 

    # def __init__(self, history_df):
    #     self.hist_df = history_df
    #     # self.command_handler = CommandHandler()
    
    # # @staticmethod
    # # def manage_history(self):
    # #     #get name of file from env
    # #     hist_file_name = self.env_settings.get('HIST_FILE_NAME', 'calc_history.csv')
    # #     path_rel_hist_folder = self.env_settings.get('HIST_FILE_PATH', '/')
    # #     path_abs_hist_folder = os.path.abspath(path_rel_hist_folder)
    # #     path_abs_hist_file = os.path.join(path_abs_hist_folder, hist_file_name)
    # #     log.debug(hist_file_name)
    # #     log.debug(path_rel_hist_folder)
    # #     log.debug(path_abs_hist_folder)
    # #     log.debug(path_abs_hist_file)
        

    # #     if (os.path.exists(path_abs_hist_file)): 
    # #         hist_df = pd.read_csv(path_abs_hist_file)
    # #         log.info("Loaded existing history file")
    # #     else: 
    # #         columns = ['operand', 'num1', 'num2', 'result']
    # #         hist_df = pd.DataFrame(columns=columns)
    # #         hist_df.to_csv(path_abs_hist_file)
        
    # #     return hist_df


    #     # os.makedirs('logs', exist_ok=True)
    #     # path_rel_log_conf = 'logging.conf'
    #     # path_abs_log_conf = os.path.abspath(path_rel_log_conf):weird
    #     #get path of file from env
            
    @staticmethod
    def run_calculations(a:Decimal, b:Decimal, operation_name:str):
        # uses functions imported from calc.operations to randomly generate one of the ops
        operation_maps = {
            'add': Calculator.add,
            'subtract': Calculator.subtract,
            'multiply': Calculator.multiply,
            'divide': Calculator.divide,
            'sqrt': Calculator.sqrt
        }


        # Unified error handling for decimal conversion
        try:
            #Test if a and b can be set to decimal
            a_decimal = Decimal(a)
            b_decimal = Decimal(b) 
            
            #Use .get to handle unknown operations from the dictionary
            curr_operation_func = operation_maps.get(operation_name) 
            result = curr_operation_func(a_decimal, b_decimal)

            if curr_operation_func:
                print(f"Result: {a} {operation_name} {b} = {result}")
                #append to hist_df
            else:
                print(f"Unknown operation: {operation_name}")

        except InvalidOperation: # not a number
            print(f"Invalid number input: {a} or {b} is not a valid number.")
        except ZeroDivisionError: # Dividing by zero
            print("An error occurred: Cannot divide by zero.")
        except Exception as e: # Catch-all for unexpected errors
            print(f"An error occurred: {e}")



    def execute(self, *args): 
        # Control the input
        # 4 inputs only 
        # while (args[0] != 'exit'):
        if len(args) != 3:
            print("Usage: calc <number1> <number2> <operation>\n <operation>: 'add' 'subtract' 'multiply' 'divide' 'sqrt' (only 1 <number)")
            return
        
        #Set arguments
        a = args[0]
        b = args[1]
        operation = args[2]
        
        #Take system args and run as a function
        self.run_calculations(a, b, operation)
