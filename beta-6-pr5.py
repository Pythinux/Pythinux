global data
try:
    f=open("userlist.pythinux","r")
    data=f.read()
    f.close()
    data=data.split("/")
    data2=[]
    for item in data:
        data2.append(item.split("|"))
    data=data2
    data2=[]
    for item in data:
        if len(item) == 3:
            data2.append(item)
    data=data2
except:
    f=open("userlist.pythinux","w")
    f.write("root|root|2/guest|password|0/user|password|1")
    f.close()
    f=open("userlist.pythinux","r")
    data=f.read()
    f.close()
    data=data.split("/")
    data2=[]
    for item in data:
        data2.append(item.split("|"))
    data=data2
    data2=[]
    for item in data:
        if len(item) == 3:
            data2.append(item)
    data=data2
global os, app_version, autologin
global username, password, user_lvl, user_type, user_type
import getpass
from time import ctime, strftime, sleep
import os
from secrets import choice

os,app_version,="Pythinux",[0,6,"PR5"]
autologin = 1
def refresh_data():
    global data
    try:
        f=open("userlist.pythinux","r")
        data=f.read()
        f.close()
        data=data.split("/")
        data2=[]
        for item in data:
            data2.append(item.split("|"))
        data=data2
        data2=[]
        for item in data:
            if len(item) == 3:
                data2.append(item)
        data=data2
    except:
        f=open("userlist.pythinux","w")
        f.write("root|root|2/guest|password|0/user|password|1")
        f.close()
        f=open("userlist.pythinux","r")
        data=f.read()
        f.close()
        data=data.split("/")
        data2=[]
        for item in data:
            data2.append(item.split("|"))
        data=data2
        data2=[]
        for item in data:
            if len(item) == 3:
                data2.append(item)
    return ""
def debug_menu():
    div()
    print("[0] Return")
    print("[1] Crash")
    print("[2] Custom Crash")
    print("[3] Crashloop")
    print("[4] Custom Crashloop")
    print("[5] Custom AutoUser")
    div()
    try:
        ch=int(input(">"))
    except:
        main()
    if ch == 1:
        crash()
    elif ch == 2:
        crash(upper(input("Reason $").replace(" ","_")),upper(input("Subreason $")).replace(" ","_"))
    elif ch == 3:
        crash("CRASH","GENERIC_CRASH",1)
    elif ch == 4:
        crash(upper(input("Reason $")),upper(input("Subreason $")),1)
    elif ch == 5:
        autologin = 1
        login(1,input("Username $"),input("Password $"),1)
    else:
        main()
def crash(reason="CRASH",subreason="GENERIC_CRASH",crash_loop=0):
    if crash_loop == 1:
        div()
        print("CRASH")
        div()
        print(f"The fatal error occured and {os} was forced to terminate itself in order to protect the hardware and software from irreversible damage.")
        div()
        print(f"{reason}:{subreason}")
        try:
            ch=input("Restart? Y/N $")
        except:
            sleep(2.5)
            crash(reason,subreason,1)
        if lower(ch) != "n":
            sleep(2.5)
        crash(reason,subreason,1)
    else:
        div()
        print("CRASH")
        div()
        print(f"The fatal error occured and {os} was forced to terminate itself in order to protect the hardware and software from irreversible damage.")
        div()
        print(f"{reason}:{subreason}")
        try:
            ch=input("Restart? Y/N $")
        except:
            crash(reason,subreason)
        if lower(ch) != "n":
            sleep(2.5)
            login()
        else:
            crash(reason, subreason)
def is_god():
    global user_lvl
    if user_lvl >= 3:
        return True
    else:
        return False
def rng(a,b):
    # Uses secrets to generate a random number for "true" randomness
    return choice(list(range(a,b+1)))
def auth():
    div()
    print("AUTHENTICATION")
    div()
    global password
    newpass=getpass.getpass("Password $")
    if password == newpass:
        return True
    else:
        return False
def br():
    div()
    input("Press ENTER to continue.\n")
    return True
def is_root():
    global user_lvl
    if user_lvl >= 2:
        return True
    else:
        return False
def div():
    print("--------------------")
    return None
def upper(inp):
    if isinstance(inp,str) == True:
        return inp.upper()
    else:
        return "[UNDEFINED]"
def lower(inp):
    if isinstance(inp,str) == True:
        return inp.lower()
    else:
        return "[UNDEFINED]"
def god_check():
    if user_lvl >= 3:
        print("God account detected.")
        return False
    else:
        return True
def userlist():
    global data
    div()
    print("GOD USERS")
    div()
    has_god = 0
    has_root = 0
    has_regular = 0
    has_guest = 0
    for item in data:
        if item[2] == "3":
            has_god = 1
            print(item[0])
    if has_god == 0:
        print("N/A")
    div()
    print("ROOT USERS")
    div()
    for item in data:
        if item[2] == "2":
            has_root = 1
            print(item[0])
    if has_root == 0:
        print("N/A")
    div()
    print("NORMAL USERS")
    div()
    for item in data:
        if item[2] == "1":
            has_regular = 1
            print(item[0])
    if has_regular == 0:
        print("N/A")
    div()
    print("GUEST USERS")
    div()
    for item in data:
        if item[2] == "0":
            has_guest = 1
            print(item[0])
    if has_guest == 0:
        print("N/A")
    br()
    main()
def scriptux():
    global os, app_version
    div()
    print(f"This version of Scriptux may have compatibility issues with the new {os}.")
    div()
    vali=0 #used to validate if the version was declared
    hasdebug=0
    endmsg=""
    file=input("Filename >")
    if file == "about:scriptux":
        print("Scriptux")
        print("Version 1a")
        print("(c) 2022 WinFan3672, all rights reserved.")
        main()
    else:
        file=file+".pyth"
        try:
            file=open(file,"r")
        except:
            print("FILE ERROR")
            main()
            import sys
            sys.exit()
        for line in file:
            if "print " in line and vali == 1:
                printf=line[6:]
                print(printf)
            elif "var input " in line and vali == 1:
                linx=line[10:]
                var=input(linx)
            elif "var print" in line and vali == 1:
                try:
                    print(var)
                except:
                    print("VARIABLE ERROR! Var not assigned")
            elif "var clear" in line and vali == 1:
                var=""
            elif "about os" in line and vali == 1:
                print(os)
            elif "about version" in line and vali == 1:
                print(version)
            elif "about scriptux" in line and vali == 1:
                print("Scriptux v1")
            elif "about manual" in line  and vali == 1:
                print("Scriptux is a scripting langauge for Pythinux written in the")
                print("Python programming language.")
                print("There isn't a manual yet. Just wait for one if ur lazy")
                print("Or you could read the code!")
            elif "nl" in line and vali == 1:
                print("\n")
            elif "endmsg " in line and vali == 1:
                endmsg=line[7:]
            elif "version=" in line:
                if "version=1" in line and vali == 0:
                    vali=1
                    continue
                else:
                    print("Version Error! Script is for older/newer version")
                    print("The version line in your script:")
                    print(line)
                    vali=2
                    break
            elif "end" in line and vali == 1:
                vali=4
                break
            else:
                continue
        file.close()
        if vali == 1:
            print("Program ended.")
        elif vali == 2:
            print("Program terminated with errors.")
        elif vali == 4:
            if endmsg == "":
                print("Program terminated using END command.")
                #Using the end command at the end of the program is not necessary, but it does allow for custom end messages!
            else:
                print(endmsg)
        else:
            print("Your program didn't provide a version!")
            print("On line 1, you need to include version=1 in order for it to work")
            scriptux()
        main()            
def main():
    global username, password, user_lvl, user_type
    god_check()
    ch=lower(input(f"{user_type}@{username} $"))
    if ch == "help":
        print(f"This build of {os} is rewritten from the ground up, and has fewer commands. Trust me, this is for the best.")
        div()
        print(f"Command list:\nabout help logoff author rewrite mul rand rng time cls")
        print(f"echo started div add sub stopwatch timer getdetails bytegen chkroot")
        print(f"quit forgot power sysinfo mod userlist timeloop sqrt area add_user")
        print(f"scriptux")
        main()
    elif ch == "about":
        div()
        print(f"{upper(os)} v{app_version[0]}.{app_version[1]}.{app_version[2]}")
        div()
        print(f"{os} is (c) 2022 WinFan3672, some rights reserved.")
        print(f"{os} is distributed under the MIT license, a flexible license\nthat gives full control over source code and no warranty.")
        div()
        main()
    elif ch == "logoff":
        login()
    elif ch == "ping":
        print("Pong")
        main()
    elif ch == "author":
        div()
        print(f"{os} was written by WinFan3672.")
        print(f"WinFan3672 is a British developer making stupid things like this.")
        div()
        print(f"To find out why WinFan3672 made this rewritten {os}, type REWRITE.")
        main()
    elif ch == "":
        main()
    elif ch == "rewrite":
        div()
        print(f"{os} was made in early 2022.")
        print(f"It was the first major project I ever worked on, while I was still learning the basics of Python.")
        print(f"One day, I decided to work on {os}, and the first thing I noticed was how messy my code was.")
        print(f"Compared to my modern code, it was a mess.")
        print(f"I knew a rewrite was in order.")
        print(f"I had already started rewriting my previous stuff, and decided to get on with it.")
        print(f"The rewrite will have a much better UI and code.")
        print(f"Hopefully, this isn't something I end up regretting :)")
        br()
        main()
    elif ch == "mul":
        print("Syntax:")
        print("mul [int] [int]")
        main()
    elif "mul " in ch:
        try:
            ch=ch.split(" ")
            if len(ch) == 3:
                try:
                    print(int(ch[1])*int(ch[2]))
                except:
                    print("Invalid use of command.")
                    print("Correct use: mul [int] [int]")
            else:
                print("MUL requires [2] parameters, and [2] parameters only.")
        except:
            print("Invalid use of command.")
            print("Correct use: mul [int] [int]")
            main()
        main()
    elif ch == "time":
        print(strftime("%x %X"))
        main()
    elif ch == "rand":
        print(rng(100000,1000000))
        main()
    elif ch == "rng":
        print("RNG generates a random number from [1st parameter] to [2nd parameter]")
        div()
        print("Correct syntax:")
        print("rng [int] [int]")
        main()
    elif "rng " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(rng(int(ch[1]),int(ch[2])))
            except:
                print("Only INT numbers are accepted.")
                main()
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"RNG requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "cls":
        for i in range(39):
            print()
        main()
    elif "echo " in ch:
        print(ch[5:])
        main()
    elif ch == "echo":
        print("echo <str>")
        main()
    elif ch == "started":
        div()
        print("GETTING STARTED GUIDE")
        div()
        print("In order to enter a list of commands, type HELP.")
        print("In order to log off, type LOGOFF.")
        main()
    elif ch == "div":
        print("Correct syntax:")
        print("div [int] [int]")
        main()
    elif "div " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(int(int(ch[1])/int(ch[2])) if int(ch[1]) % int(ch[2]) == 0 else int(ch[1])/int(ch[2]))
            except:
                print("Incorrect syntax.")
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"RNG requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "add":
        print("Correct syntax:")
        print("add [int] [int]")
        main()
    elif "add " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(int(ch[1])+int(ch[2]))
            except:
                print("Incorrect syntax.")
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"RNG requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "sub":
        print("Correct syntax:")
        print("sub [int] [int]")
        main()
    elif "sub " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(int(ch[1])-int(ch[2]))
            except:
                print("Incorrect syntax.")
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"RNG requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "timer":
        print("Correct syntax:")
        print("timer [seconds(int)]")
        main()
    elif "timer " in ch:
        ch=int(ch[6:])
        while ch > 0:
            print(ch)
            sleep(1)
            ch -= 1
        main()
    elif ch == "stopwatch":
        print("[Press CTRL+C To Exit]")
        i = 1
        try:
            while True:
                print(i)
                i += 1
                sleep(1)
        except:
            main()
    elif ch == "getdetails":
        if is_root() == True:
            print(f"Username: {username}")
            newpass=""
            for item in password:
                newpass+="*"
            print(f"Password: {newpass}")
            main()
        else:
            print("You need to be root to access this command.")
            main()
    elif ch == "bytegen":
        print("Correct syntax:")
        print("bytegen [number of bytes (int)]")
        main()
    elif "bytegen " in ch:
        ch=ch.split(" ")
        if len(ch) == 2:
            try:
                for i in range(int(ch[1])):
                    print(f"{rng(0,1)} {rng(0,1)} {rng(0,1)} {rng(0,1)} {rng(0,1)} {rng(0,1)} {rng(0,1)} {rng(0,1)}")
            except:
                print("An error occured.")
                main()
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"BYTEGEN requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "chkroot":
        print(is_root())
        main()
    elif ch == "quit":
        import sys
        sys.exit()
    elif ch == "forgot":
        print("Warning! This tool will ask you for your password.")
        print("If you enter it wrong, you will be logged out.")
        print("By using this utility, you agree to this.")
        div()
        print("[1] Enter Tool")
        print("[0] Return")
        div()
        try:
            ch=int(input(">"))
        except:
            main()
        if ch == 1:
            if auth() == True:
                main()
            else:
                login()
        else:
            main()
    elif ch == "power":
        print("power [num1] [num2]")
        print("Outputs [num1] to the power of [num2]")
    elif "power " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(str("{:,}".format(float(ch[1]) ** float(ch[2]))))
            except:
                print("ERROR.")
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"POWER requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "sysinfo":
        import platform
        print(platform.system(),platform.uname()[2])
        print("OS:",platform.platform())
        try:
            import tkinter as tk
            root = tk.Tk()
        except:
            root = "N/A"
        try:
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
        except:
            screen_width = "N/A"
            screen_height = "N/A"
        try:
            root.withdraw()
        except:
            pass
        print("Screen width:",screen_width)
        print("Screen height:",screen_height)
        import sys
        v=platform.python_version()
        print("Python",v)
        th=platform.architecture()
        th=th[0]
        print("Architecture=",th)
        cpu=platform.processor()
        print("CPU:",cpu)
        br()
        main()
    elif ch == "debug" or ch == "root":
        if is_root() == True and auth() == True:
            debug_menu()
        else:
            div()
            print("An error occured:")
            print("[-] You are not a ROOT user")
            print("OR:")
            print("[-] You enter an incorrect password.")
            div()
            main()
    elif ch == "mod":
        div()
        print("mod [num1] [num2]")
        print("Outputs [num] % [num2]")
        main()
    elif "mod " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(str("{:,}".format(float(ch[1]) % float(ch[2]))))
            except:
                print("An error occured.")
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"MOD requires [2] parameters, got [{len(ch)-1}].")
        main()
    elif ch == "userlist":
        if is_root() == True:
            userlist()
        else:
            print("Only ROOT users can access this menu.")
            main()
    elif ch == "timeloop":
        if is_root() == True:
            print("Enter CTRL+C to exit.")
            while True:
                try:
                    print(strftime("%x %X"))
                    sleep(1)
                except:
                    main()
        else:
            print("ROOT required for this command.")
            main()
    elif ch == "sqrt":
        print("sqrt [float]")
        print("Does sqare root of [float].")
        main()
    elif ch == "area":
        div()
        print("Area Menu")
        div()
        print("[1] Rectangle")
        print("[2] Triangle")
        print("[3] Circle")
        div()
        try:
            ch=int(input(">"))
        except:
            main()
        if ch == 1:
            try:
                print(int(input("Base $")) * int(input("Height $")))
            except:
                print("@ERROR")
            main()
        elif ch == 2:
            try:
                print(int(input("Base $")) * int(input("Height $")) / 2)
            except:
                print("@ERROR")
            main()
        elif ch == 3:
            from math import pi
            try:
                print((int(input("Radius $")) ** 2) * pi)
            except:
                print("@ERROR")
            main()
        else:
            main()
    elif "sqrt " in ch:
        ch=ch.split(" ")
        try:
            from math import sqrt
            print(sqrt(float(ch[1])))
        except:
            print("An error occured.")
        main()
    elif ch == "add_user":
        if is_root() == True:
            f=open("userlist.pythinux","r")
            d=f.read()
            f.close()
            f=open("userlist.pythinux","w")
            base1=input("Username $")
            base2=input("Username $")
            base3=input("UserLVL  $")
            try:
                if int(base3) >= user_lvl:
                    base3 = str(user_lvl)
                    print(f"[To prevent privelege escalation, {os} has automatically reduced the user level you chose.")
            except:
                pass
            f.write(d+f"/{base1}|{base2}|{base3}")
            f.close()
            refresh_data()
            print("Added to userlist.")
            main()
        else:
            print("You must be a ROOT user to access this.")
    elif ch == "scriptux":
        if is_root() == True:
            scriptux()
        else:
            print("Only ROOT users can access this.")
            main()
    else:
        print(f"{upper(ch)} IS NOT A VALID COMMAND, PROGRAM OR MANUAL.")
        main()
        
def start(lvl):
    global username, password, user_lvl, user_type
    user_lvl = lvl
    if user_lvl == 0:
        user_type="guest"
    elif user_lvl == 1:
        user_type = "user"
    elif user_lvl == 2:
        user_type = "root"
    elif user_lvl == 3:
        user_type = "god"
    else:
        user_type="[INVALIDUSER]"
    print(f"Welcome to {os}.")
    print(f"[{os} v{app_version[0]}.{app_version[1]}.{app_version[2]}]")
    div()
    if user_lvl == 0:
        print("You are logged in on a guest account.")
        print("Guest accounts have limited access to commands and cannot run programs.")
    elif user_lvl == 1:
        pass
    elif user_lvl == 2:
        print("You are logged in as a root account.")
        print("If you do not know what this means, type LOGOUT right now.")
        print("DO NOT USE A ROOT ACCOUNT AS YOUR DAILY DRIVER ACCOUNT.")
    elif user_lvl == 3:
        pass
    else:
        print("[Error: The account type is invalid.]")
        login()
    main()
def login(al=0,al_username="root",al_password="root"):
    global username, password, user_lvl, user_type, autologin, data
    if al == 1:
        base=f"{al_username}:{al_password}"
        username,password=f"{al_username}",f"{al_password}"
        autologin = 0
    else:
        div()
        print(f"{upper(os)} LOGIN SYSTEM")
        div()
        print("Enter your login details.")
        print("If they are valid, you will be logged in.")
        div()
        print("Username = guest\nPassword = password\nFor a guest account")
        div()
        username=input("Username $")
        password=getpass.getpass("Password $")
        div()
        base=f"{username}:{password}"
    for item in data:
        try:
            if base == f"{item[0]}:{item[1]}":
                start(int(item[2]))
        except:
            continue
    print("Username or password is invalid.")
    login()
login(autologin)
