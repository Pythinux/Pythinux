import math

def rect(base, height):
    return base * height

def triangle(base, height):

    return 0.5 * base * height

def circle(rad):

    return math.pi * (rad ^ 2)

def main(args):
    if "-r" in args and len(args) == 3:
        print(rectangle(args[1], args[2]))
    elif "-t" in args and len(args) == 3:
        print(triangle(args[1], args[2]))
    elif "-c" in args and len(args) == 2:
        print(circle(args[1]))
    else:
        runCommand(currentUser, "man area")
