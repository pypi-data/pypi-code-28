
from functools import reduce

def prod( data ):
    return reduce(lambda x, y : x* y, data)