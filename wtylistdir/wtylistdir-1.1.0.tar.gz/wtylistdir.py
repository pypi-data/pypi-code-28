import os

__path=os.getcwd()

def listdir(path=__path):
    result = os.listdir(path)
    return result


