from decimal import Decimal, InvalidOperation
import sys

from commands import Command

from decimal import Decimal, InvalidOperation

from plugins.calc.calculator import Calculator


class CalcCommand(Command): 

    # def __init__(self):
    #     self.command_handler = CommandHandler()

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
            curr_operation = operation_maps.get(operation_name) 
            
            if curr_operation:
                print(f"Result: {a} {operation_name} {b} = {curr_operation(a_decimal, b_decimal)}")
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
