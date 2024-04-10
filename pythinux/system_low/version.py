def get():
    return "Pythinux {}".format(".".join([str(x) for x in version]))

def getfloat():
    return float("{}.{}".format(version[0], version[1]))

def main(args):
    print(get())
