libargs = load_program("libargs", currentUser, libMode=True)

parser = libargs.ArgumentParser("calc", description="Performs arithmetic calculations")
parser.add_argument("calculation", nargs="+", help="Caluclation to perform")

def calc(calculation):
    assertTrue(isinstance(calculation, str))
    return doCalc(calculation)

def main(args):
    args = parser.parse_args(args)
    print(calc(" ".join(args.calculation)))
