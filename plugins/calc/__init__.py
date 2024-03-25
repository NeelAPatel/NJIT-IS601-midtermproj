from decimal import Decimal, InvalidOperation
import os
import sys

import pandas as pd

from commands import Command

from decimal import Decimal, InvalidOperation

from plugins.calc.calculator import Calculator
import logging as log



class CalcCommand(Command): 


    @staticmethod
    # def run_calculations(self, a:Decimal, b:Decimal, operation_name:str):
    def run_calculations(self, *args):
        # uses functions imported from calc.operations to randomly generate one of the ops
        operation_maps = {
            'add': Calculator.add,
            'subtract': Calculator.subtract,
            'multiply': Calculator.multiply,
            'divide': Calculator.divide,
            'sqrt': Calculator.sqrt
        }

        sign_maps = {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '/',
            'sqrt': 'sqrt'
        }

        operation_name = args[0]
        a = args[1]
        b = b = args[2] if len(args) > 2 else None

        # Unified error handling for decimal conversion
        try:
            #Test if a and b can be set to decimal 
            a_decimal = Decimal(a)
            b_decimal = Decimal(b) if b is not None else None
            
            #Use .get to handle unknown operations from the dictionary
            curr_operation_func = operation_maps.get(operation_name) 
            curr_operation_sign = sign_maps.get(operation_name)

            if (operation_name == "sqrt"): 
                result = curr_operation_func(a_decimal)
                a,b = "",a # flip for formatting in csv
            else: 
                result = curr_operation_func(a_decimal, b_decimal)


            if curr_operation_func:
                print(f"Result: {a} {operation_name} {b} = {result}")
                self.save_operation("add",a, curr_operation_sign, b, result)
            else:
                print(f"Unknown operation: {operation_name}")

        except InvalidOperation: # not a number
            print(f"Invalid number input: {a} or {b} is not a valid number.")
        except ZeroDivisionError: # Dividing by zero
            print("An error occurred: Cannot divide by zero.")
        except Exception as e: # Catch-all for unexpected errors
            print(f"An error occurred: {e}")


    def defaultMessage(self, *args): 
        print('Usage: ')
        print('    calc <operation> <num1> <num2 if needed>')
        print('')
        print('Operations: ')
        print('    add <num1> <num2>       adds two numbers (num1+num2)')
        print('    subtract <num1> <num2>  subtract num2 from num1 (num1-num2)')
        print('    multiply <num1> <num2>  multiplies two numbers (num1*num2)')
        print('    divide <num1> <num2>    divide num1 by num2 (num1/num2)')
        print('    sqrt <num1>             square root of num1')
    
    # @staticmethod
    def save_operation(self, *args):
        print("save_op", args)
        from plugins.history import HistoryCommand as histComm
        hist_instance = histComm()
        hist_instance.add(*args)
        # from plugins.history.hi import HistoryCommand  as histComm.add( *args)

    def execute(self, *args): 
        if len(args) >= 3:
            self.defaultMessage(*args)
            return
        
        #Set arguments
        # operation = args[0]
        # a = args[1]
        # b = args[2] if args[2] is not None else None
        
        #Take system args and run as a function
        self.run_calculations(self,*args)
