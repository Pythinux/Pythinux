import os
if args:
    args = " ".join(args)
    os.mkdir(args)
else:
    div()
    print("md [directory]")
    div()
    print("Creates [directory] if it does not exist.")
    div()
