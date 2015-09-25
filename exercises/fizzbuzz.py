# Standard fizz buzz, using a composed function. 

def make_response(num, div, word):
    if type(num) is str:
        return num
    else:
        return word if num % div == 0 else num

def fizz_buzz(x):
    return make_response(x, 15, "fizz_buzz")

def buzz(x):
    return make_response(x, 5, "Buzz")

def fizz(x):
    return make_response(x, 3, "Fizz")

def compose(x, y):
        return lambda z:(x(y(z)))

fB = compose(compose(fizz_buzz, buzz), fizz)

for i in map(fB, range(1,101)):
    print i
