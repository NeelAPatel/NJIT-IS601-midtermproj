from decimal import Decimal, InvalidOperation
import os
import sys

import pandas as pd

from commands import Command

from decimal import Decimal, InvalidOperation

from plugins.calc.calculator import Calculator
import logging as log



class CalcCommand(Command): 

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

        #Works
        if operation_name not in operation_maps:
            log.error(f"Unknown operation: {operation_name}")
            return
        
        # Convert inputs to Decimal and validate
        try:
            a_decimal = Decimal(a)
            b_decimal = Decimal(b)
        except InvalidOperation as e:
            log.error(f"Invalid number input: {e}")
            return

        try: 
            # Perform the calculation
            curr_operation_func = operation_maps[operation_name]
            curr_operation_sign = sign_maps[operation_name]
            result = curr_operation_func(a_decimal, b_decimal)

            print(f"Result: {a} {operation_name} {b} = {result}")
            self.save_operation("add",a, curr_operation_sign, b, result)            
        except ValueError: 
            log.error("An error occurred: Cannot divide by zero")


    def defaultMessage(self, *args): 
        message = (
            'Usage: \n'
            '    calc <operation> <num1> <num2 if needed>\n'
            '\n'
            'Operations: \n'
            '    add <num1> <num2>       adds two numbers (num1+num2)\n'
            '    subtract <num1> <num2>  subtract num2 from num1 (num1-num2)\n'
            '    multiply <num1> <num2>  multiplies two numbers (num1*num2)\n'
            '    divide <num1> <num2>    divide num1 by num2 (num1/num2)'
        )
        print(message)
        
    def save_operation(self, *args):
        from plugins.history import HistoryCommand as histComm
        hist_instance = histComm()
        hist_instance.add(*args)

    def execute(self, *args): 
        if len(args) == 0: 
            self.defaultMessage(*args)
            return
        elif not  2 < len(args) < 4:
            log.error("Error: Incorrect number of arguments for calc")
            return
        

        try: 
            operation = args[0]
            a = args[1]
            b = b = args[2]

            #Take system args and run as a function
            self.run_calculations(a, b, operation)
        except Exception as e:
            # Catch-all for any unexpected errors
            log.error(f"An unexpected error occurred: {e}")