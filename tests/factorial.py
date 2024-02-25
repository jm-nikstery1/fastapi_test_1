class MyFactorial:
    def __init__(self):
        pass

    def factorial(self, n):
        if n < 0:
            n = -n
        val = 1

        while n > 0:
            val *= n
            n -= 1

        return val