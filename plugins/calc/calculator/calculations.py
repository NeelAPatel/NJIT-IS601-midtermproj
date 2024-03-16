from decimal import Decimal
from typing import Callable, List

from plugins.calc.calculator.calculation import Calculation

class Calculations: 
    #Stores all 'Calculation's performed
    #history is typeforced to be of type List, and each element will be of Calculation type
    history: List[Calculation] = [] 


    # @Classmethod = affects ALL instances. any instance can add to the one singular history variable
    # cls keyword means itself but class type. affects all classes. 
    # self keyword therefore works for instances only
    @classmethod
    def add_to_history(cls, calculation: Calculation): 
        """Appends newest calculation to history"""
        cls.history.append(calculation)
    
    @classmethod
    def clear_history(cls): 
        """Empties calculation history"""
        cls.history.clear() #empties the list

    @classmethod
    def get_history(cls) -> List[Calculation]:
        """Return full history of calculations"""
        return cls.history
    
    # Returns latest Calculation element
    # -1 index = last index by looping backwards
    @classmethod
    def get_latest_calc(cls) -> Calculation:
        """Return latest calculation"""
        if cls.history: #If history exists
            return cls.history[-1]
        return None
    
    @classmethod
    def find_by_operation(cls, operation_name: str) -> List[Calculation]:
        """Find by matching requested operation and return list of matching calculations"""
        # List comprehension
        return [calc for calc in cls.history if calc.operation.__name__ == operation_name]