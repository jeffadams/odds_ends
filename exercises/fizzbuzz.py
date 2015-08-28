# Standard fizz buzz, using a composed function. 

def compose(x, y):
    return lambda z:(x(y(z)))

def makeResponse(num, div, word):
    if type(num) is str:
        return num
    else:
        return word if num % div == 0 else num

def fizzBuzz(x):
    return makeResponse(x, 15, "FizzBuzz")

def buzz(x):
    return makeResponse(x, 5, "Buzz")

def fizz(x):
    return makeResponse(x, 3, "Fizz")

fB = compose(compose(fizzBuzz, buzz), fizz)
for i in map(fB, range(1,101)):
    print i
