import time

def date():
    return time.strftime("%d-%M-%Y")

def time():
    return time.strftime("%H:%M:%S %z")

def datetime():
    return "{} {}".format(date(), time())
