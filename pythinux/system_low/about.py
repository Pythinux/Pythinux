import time
def main(args):
    friendlyVersion = ".".join([str(x) for x in version])
    year = time.strftime("%Y")

    div()
    print("{} {}".format(osName, friendlyVersion))
    print("(c) 2021-{} Pythinux, some rights reserved.".format(year))
    div()
