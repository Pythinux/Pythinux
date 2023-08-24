import math
if args == ["-r"]:
    div()
    print("area -r <base> <height>")
    div()
    print("Returns <base> * <height>")
    div()
elif "-r" in args and len(args) == 3:
    try:
        args[1] = float(args[1])
        args [2] = float(args[2])
        print(args[1]*args[2])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
elif args == ["-t"]:
    div()
    print("area -t <base> <height>")
    div()
    print("Returns 1/2 * <base> * <height>")
    div()
elif "-t" in args and len(args) == 3:
    try:
        args[1] = float(args[1])
        args [2] = float(args[2])
        print(1/2 * args[1]*args[2])
    except Exception as e:
        print(f"{type(e).__name__}: {e}")    
elif args == ["-c"]:
    div()
    print("area -r <radius>")
    div()
    print("Returns the area of a circle based on its radius")
    div()
elif "-c" in args and len(args) == 2:
    try:
        print(math.pi * (float(args[1])**2))
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
else:
    div()
    print("area [args]")
    div()
    print("args:")
    print("    -r: rectangle")
    print("    -t: triangle")
    print("    -c: circle")
    div()
