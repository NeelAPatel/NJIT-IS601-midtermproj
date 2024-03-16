# These are operation functions, meant to be called and passed as parameters to use.
from decimal import Decimal # Importing Decimal to typeforce 

# a and b are forced to be Decimal type upon use, and return type will be of Decimal format as well
def add(a: Decimal, b: Decimal) -> Decimal: 
    #sum of a + b
    return a + b; 

def subtract (a: Decimal, b: Decimal) -> Decimal:
    return a - b;

def multiply (a: Decimal, b: Decimal) -> Decimal:
    return a * b;

def divide (a: Decimal, b: Decimal) -> Decimal:
    # since you can divide by 0, ensure it fails gracefully by raising error
    if (b == 0): 
        raise ValueError("Cannot divide by zero.")
    return a / b;

def sqrt (a: Decimal) -> Decimal:
    return Decimal(a).sqrt()