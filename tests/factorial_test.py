from .factorial import MyFactorial
import math

my_class = MyFactorial()

def test_factorial_zero():
    #my_class = MyFactorial()
    assert my_class.factorial(0) == 1

def test_factorial_10():
    #my_class = MyFactorial()
    assert my_class.factorial(10) == math.factorial(10)

def test_factorial_1000():
    #my_class = MyFactorial()
    assert my_class.factorial(1000) == math.factorial(1000)