print("DeprecationWarning: `removed` is deprecated, use `pkm remove` instead.")
cmd = "pkm remove " + " ".join(args)
main(currentUser,cmd)