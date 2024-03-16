# Class is created and used to specifically handle ONE calculation, nothing more

from decimal import Decimal # Importing Decimal to typeforce 
from typing import Callable # Allows hinting to operation variable that its a callable function


class Calculation: 
    # Callable [input params types, output param type]; since you need two inputs, its [decimal,decimal]
    def __init__ (self,a: Decimal,b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
         # Instance variables
        self.a = a
        self.b = b
        self.operation = operation # This allows any operation function to be triggered by calculation

    # Wraps the Constructor of this class for an alternative way 
    # Allows use without instantiating the class directly
    @staticmethod
    def create(a: Decimal,b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        return Calculation(a,b,operation)


    #Used to be get_result
    def perform(self) -> Decimal: 
        # Calls the stored operation function AS operation() and uses a,b on it
        # -- basically renames operations into a singular function since 
        # -- all 4 use same number and type of parameters
        return self.operation(self.a, self.b)
    
    #returns a string representation of the specific Calculation instance
    def __repr__(self) -> str:
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"