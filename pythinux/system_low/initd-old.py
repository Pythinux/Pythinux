import sys
import traceback
if args == ["--init"]:
    try:
        with open(f"home/{currentUser.username}/init.d") as f:
            run_script(f,currentUser)
    except Exception as e:
        print(traceback.format_exc())
elif args == ["--add"]:
    div()
    print("main --add [command]")
    div()
    print("Adds the command to the start of the init.d file.")
    div()
elif args == ["--remove"]:
    div()
    print("initd --remove [command]")
    div()
    print("Removes a command from the init script")
    div()
elif "--remove" in args and args[0] == "--remove":
    with open(f"home/{currentUser.username}/init.d") as f:
        d=f.readlines()
        x=[]
        args = " ".join(args[1:])
        for i in d:
            if not args in i:
                x.append(i)
    with open(f"home/{currentUser.username}/init.d","w") as f:
        f.writelines(x)
elif "--add" in args and args[0] == "--add":
    args.pop(0)
    main(currentUser,f"initd --remove {' '.join(args)}")
    with open(f"home/{currentUser.username}/init.d") as f:
        d=f.readlines()
        d.insert(0," ".join(args))
    with open(f"home/{currentUser.username}/init.d","w") as f:
        f.write("\n".join(d))
elif args == ["--view"]:
    main(currentUser,f"cat home/{currentUser.username}/init.d")
else:
    div()
    print("initd [args]")
    div()
    print("initd is an init system that is run on startup.")
    div()
    print("--init: runs init script")
    print("--view: shows the init script")
    print("--add: adds a command to the init script")
    print("--remove: removes a command from the init script")
    div()
