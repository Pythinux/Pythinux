def get():
    return "Pythinux {}".format(".".join([str(x) for x in version]))

def main(args):
    print(get())
