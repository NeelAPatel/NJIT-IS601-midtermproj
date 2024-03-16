from typing import Callable
from plugins.calc.calculator.calculation import Calculation
from plugins.calc.calculator.calculations import Calculations
from plugins.calc.calculator.operations import add, subtract, multiply, divide, sqrt
from decimal import Decimal # Importing Decimal to typeforce 


# Main calculator class
class Calculator:


    @staticmethod
    def _perform_operation(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> Decimal:
        # create instance of a single calculation
        myCalculation = Calculation.create(a,b, operation)

        #using Calculation class itself bc we are doing it for the entire class
        Calculations.add_to_history(myCalculation)
        return myCalculation.perform()


    # @staticmethod = GLOBALLY accessible, does NOT have access to outside values/instance varibales
    # -- strict job is to take input vars => redirect. little to no calculation
    # -- Also may return result. AKA just an action method
    # Method = attached inside a class

    # Instance of Calculation-class is created, storing a,b,operation
    # THEN actual calculation is performed while returning
    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        # Call current class's owon _perform_operation on add operation
        return Calculator._perform_operation(a,b, add)
    
    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        # Call current class's owon _perform_operation on subtract operation
        return Calculator._perform_operation(a,b, subtract)
    
    @staticmethod
    def multiply (a: Decimal, b: Decimal) -> Decimal:
        # Call current class's owon _perform_operation on multiply operation
        return Calculator._perform_operation(a,b, multiply)
    
    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        # Call current class's owon _perform_operation on divide operation
        return Calculator._perform_operation(a,b, divide)
    
    @staticmethod
    def sqrt(a: Decimal) -> Decimal:
        # Call current class's owon _perform_operation on sqrt operation
        return Calculator._perform_operation(a, sqrt)
