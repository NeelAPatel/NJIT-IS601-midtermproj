from decimal import Decimal, InvalidOperation
import os
import sys

import pandas as pd

from commands import Command

from decimal import Decimal, InvalidOperation

from plugins.calc.calculator import Calculator
import logging as log



class CalcCommand(Command): 

    # @staticmethod
    # def run_calculations(self, *args):
    def run_calculations(self, a:Decimal, b:Decimal, operation_name:str):
        # uses functions imported from calc.operations to randomly generate one of the ops
        operation_maps = {
            'add': Calculator.add,
            'subtract': Calculator.subtract,
            'multiply': Calculator.multiply,
            'divide': Calculator.divide
        }

        sign_maps = {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '/'
        }

        # Unified error handling for decimal conversion
        try:
            #Test if a and b can be set to decimal 
            a_decimal = Decimal(a)
            b_decimal = Decimal(b) if b is not None else None
            
            #Use .get to handle unknown operations from the dictionary
            curr_operation_func = operation_maps.get(operation_name) 
            curr_operation_sign = sign_maps.get(operation_name)
            result = curr_operation_func(a_decimal, b_decimal)


            if curr_operation_func:
                print(f"Result: {a} {operation_name} {b} = {result}")
                self.save_operation("add",a, curr_operation_sign, b, result)
            else:
                log.error(f"Unknown operation: {operation_name}")

        except InvalidOperation: # not a number
            log.error(f"Invalid number input: {a} or {b} is not a valid number.")
        except ZeroDivisionError: # Dividing by zero
            log.error("An error occurred: Cannot divide by zero.")
        except Exception as e: # Catch-all for unexpected errors
            log.error(f"An error occurred: {e}")


    def defaultMessage(self, *args): 
        print('Usage: ')
        print('    calc <operation> <num1> <num2 if needed>')
        print('')
        print('Operations: ')
        print('    add <num1> <num2>       adds two numbers (num1+num2)')
        print('    subtract <num1> <num2>  subtract num2 from num1 (num1-num2)')
        print('    multiply <num1> <num2>  multiplies two numbers (num1*num2)')
        print('    divide <num1> <num2>    divide num1 by num2 (num1/num2)')
        
    def save_operation(self, *args):
        from plugins.history import HistoryCommand as histComm
        hist_instance = histComm()
        hist_instance.add(*args)

    def execute(self, *args): 
        if len(args) == 0: 
            self.defaultMessage(*args)
            return
        elif len(args) > 3:
            log.error("Error: Too many arguments for calc")
            self.defaultMessage(*args)
            return
        

        try: 
            operation = args[0]
            a = args[1]
            b = b = args[2] if len(args) > 2 else None
            #Take system args and run as a function
            # self.run_calculations(self,*args)
            self.run_calculations(self, a, b, operation)
            
        except IndexError: 
            log.error("Error: Missing arguments. Please follow Usage guide")
            self.defaultMessage()
