import os
if args == ["--reset"]:
    os.remove("config/autologin.cfg")
elif args:
    saveAL(" ".join(args))    
else:
    div()
    print("autologin <username>")
    div()
    print("Sets <username> as the autologin username.")
    div()
    print("autologin --reset")
    print("(Disables autologin)")
    div()
