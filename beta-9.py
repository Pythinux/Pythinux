global data
global consent_mode
consent_mode = 0
import os.path
from platform import uname
from time import strftime as stime
global stdlib
global mem,bmem
mem=0
bmem=0
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
global os_name, app_version, autologin
global username, password, user_lvl, user_type, user_type
import getpass
from time import ctime, strftime, sleep
import os
from secrets import choice

# OS INFORMATION CONTAINED HERE
os_name,app_version,="Pythinux",[0,9,0]
autologin = 1
def cman_demo():
    ch=input("cman_demo %")
    if ch == "cman":
        print("For a list of installed manuals, type `cman /`")
        print("To open a manual, type `cman <manual>")
        cman_demo()
    elif ch == "help":
        print("help cman return")
        cman_demo()
    elif ch == "cman /":
        print("Searching for manuals...")
        div()
        print("Installed Manuals")
        div()
        print("test\ntest2\ntest3")
        div()
        cman_demo()
    elif ch == "cman test":
        print("This is a test manual.")
        cman_demo()
    elif ch == "cman test2" or ch == "cman test3":
        print("This is also a test manual.")
        cman_demo()
    elif ch == "return":
        main()
    else:
        print("Bad command or file name.")
        cman_demo()
def terminal():
    termin = input(">>>")
    if termin == "%%exit":
        main()
    else:
        os.system(termin)
        terminal()
    terminal()
def is_file(fn):
    return os.path.isfile(os.getcwd()+f"/{fn}")
def vim_editor(fn=""):
    if fn == "":
        fn = input("File Name >>") + ".vimx"
    try:
        f = open(fn,"a")
        data=f.read()
        f.close()
        data=data.split("\n")
        for item in data:
            print(item)
    except:
        pass
    f = open(fn,"w")
    div()
    print("Press CTRL+C to exit")
    div()
    try:
        while True:
            f.write(input(">>"))
            f.write("\n")
    except:
        f.close()
    main()
def vim(ch=""):
    if ch == "":
        logo = ['# ##### # ', '# # # ##   ## ', '# # # # # # # ', '# # # #  #  # ', ' #   #  # # # ', '  # #   # # # ', '   #   #### # ']
        for l in logo:
            pass
        print("[1] New / Open File")
        print("[2] Read File")
        print("[3] Delete File")
        print("[4] Overwrite File")
        print("[5] Backup File")
        print("[6] Restore Backup")
        print("[7] Migrate vim.txt to VIMX")
        print("[8] Delete Backup")
        print("[9] Delete vim.txt")
        print("[10] File List")
        print("[0] Exit")
        div()
        try:
            ch=int(input(">"))
        except:
            main()
    else:
        vim_editor(ch)
    div()
    if ch == 1:
        vim_editor()
    elif ch == 2:
        try:
            f = open(input("File Name >>") + ".vimx")
            data=f.read()
            f.close()
            data=data.split("\n")
            for item in data:
                print(item)
            br()
            main()
        except:
            main()
    elif ch == 3:
        try:
            os.remove(input("File name >>")+".vimx")
        except:
            pass
        main()
    elif ch == 4:
        fn = input("File Name >>") + ".vimx"
        try:
            os.remove(fn)
        except:
            pass
        vim_editor(fn)
    elif ch == 5:
        fn = input("File Name >>")
        try:
            f = open(fn+".vimx","r")
            dataa = f.read()
            f.close()
            f = open(fn+".vimbackup","w")
            f.write(dataa)
            f.close()
            print("Backed up file.")
            main()
        except:
            print("Failed to back up file.")
            main()
    elif ch == 6:
        fn = input("File Name >>")
        try:
            f = open(fn+".vimbackup","r")
            dataa=f.read()
            f.close()
            f = open(fn+".vimx","w")
            f.write(dataa)
            f.close()
            print("Restored file.")
            main()
        except:
            print("Failed to restore file.")
            main()
    elif ch == 7:
        try:
            f=open("vim.txt","r")
            dataas=f.read()
            f.close()
            f=open("vim_legacy.vimx","w")
            f.write(dataa)
            f.close()
            print("To load, open \"vim_legacy\"")
        except:
            print("Failed to load VIM.TXT")
        main()
    elif ch == 8:
        try:
            os.remove(input("File name >>")+".vimbackup")
        except:
            pass
        main()
    elif ch == 9:
        try:
            os.remove("vim.txt")
        except:
            pass
        main()
    elif ch == 10:
        path = os.getcwd()
        dirlist = os.listdir(path)
        for item in dirlist:
            isFile = os.path.isfile(item)
            if isFile == True and item.endswith(".vimx"):
                item = item.replace(".vimx", "")
                print(item)
            else:
                continue
        br()
        vim()
    else:
        main()
def clear_screen():
    res=uname()
    os.system("cls" if res[0] == "Windows" else "clear")
def sha256(text):
    import hashlib
    hashed_string = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return hashed_string
def install_stdlib():
    global stdlib
    try:
        del(stdlib)
    except:
        pass
    try:
        import stdlib
    except:
        pass
def future_features_2():
    div()
    print("Future Features [Page II]")
    div()
    print("[1] Custom Manual")
    print(f"[2] {os_name} Folder")
    print("[<] Previous Page")
    try:
        ch=input(">")
    except:
        future_features_2()
    if ch == "1":
        man("cman")
        future_features_2()
    elif ch == "2":
        print("A Pythinux sub-folder will exist in the current working directory.")
        print("Programs can be installed and run there, documents can be stored and scripts stored as well.")
        div()
        print("Example Directory Structure")
        div()
        print("> Pythinux")
        print("   > Users")
        print("      > root")
        print("         > Documents")
        print("         > Scripts")
        print("         > Vim Files")
        print("         > User Settings")
        print("            > os_settings.toml")
        print("            > alias.pythinux")
        print("            > .user_alias_use")
        print("         > Programs")
        print("            > someprogram_helper")
        print("         > Program Data")
        print("   > Program Files")
        print("      > someprogram")
        print("         > settings.data")
        print("         > someprogram.zip")
        print("   > System Settings")
        print("      > .autologin")
        print("      > .startup")
        print("      > userlist.pythinux")
        print("      > aliases.pythinux")
        print("      > .noalias")
        print("   > Cached Data")
        print("      > someprogram.cache")
        print("   > Custom Manuals")
        print("      > test.cman")
        print("      > test2.cman")
        print("      > test3.cman")
        div()
        print("This system will allow for a much more organised and efficient system for having multiple users, and allows for much more advanced OS integration.")
        br()
        future_features_2()
    elif ch == "9" or ch == "<":
        future_features()
    else:
        future_features_2()
def future_features(ch="",return_mode = 0):
    div()
    print("Future Features")
    div()
    print("[1] Scripting Improvements")
    print("[2] WINHUB / LINUXHUB")
    print("[3] Wget")
    print("[4] Standard Library")
    print("[5] RemoveUser Command")
    print("[6] SZIPS improvements")
    print("[7] Interactive Help Hub")
    print("[8] Files Improvements")
    print("[9] Other Additions")
    print("[>] Next Page")
    div()
    if ch == "":
        try:
            ch = input(">")
        except:
            main()
    if ch == "1":
        print("[-] FILES and MAN will have full integration with Scripting.")
        print("[-] Infinite Loop Mode will allow for commands underneath the Infinite Loop line to run forever without interruption.")
        print("[-] Variables")
        print("   [-] I can do it, in fact, I have a demo.")
        br()
        if return_mode == 0:
                main()
        else:
            return None
    elif ch == "2":
        print("1 WinHub")
        div()
        print("WinHub is a program that performs various tasks exclusive to Windows:")
        print("[-] Sound playing")
        print("[-] Registry editing")
        print("[-] Clearing DNS resolver cache")
        print("[-] Pinging a server to test Internet")
        print("[-] Shutdown")
        print("[-] etc.")
        div()
        print("2 LinuxHub")
        div()
        print("LinuxHub performs various tasks exclusive to Linux:")
        print("[-] APT installs")
        print("[-] Pacman installs")
        print("[-] Updating packages")
        print("[-] etc.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "3":
        print("WGET is very similar to CAT, except it automatically works out the file name to use")
        print("WGET requires a URL and saves it to the relevant file.")
        br()
        main()
    elif ch == "4":
        print("The Pythinux standard library will add extra functionality to SZIPS programs, which can be taken advantage of.")
        print("To add SZIPS functionality to a program, add:")
        print("from stdlib import *")
        div()
        print("To the top of the file.")
        print("Example features:")
        print("[-] Clear screen")
        print("[-] Change terminal colour")
        print("[-] etc.")
        div()
        print("[Ideas not finalised, so I have little to no idea about what to do.]")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "5":
        print("RemoveUser will list all users inside the userfile and ask you which one to remove.")
        print("You can only remove users with user levels lower than the current logged-in user.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "6":
        print("[ ] RUN command will be able to use a parameter for a file name")
        print("[-] Standard Library")
        print(f"[-] Potential I/O with {os_name}.")
        print("[-] etc.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "7":
        div()
        print("Interactive help will be able to provide detailed documentation for every command.")
        print("Entering it will work like this:")
        div()
        print("root@root $ interactive_help")
        print("interactive_help $ ")
        div()
        print("Interactive help will have a terminal-like syntax, where you can type a command and get help on it:")
        div()
        print("interactive_help $ man")
        print("`man` is a manual system that prints out preinstalled manuals on your computer.")
        print("To open a manual, type `man <manual>`, replacing <manual> with the name of the manual.")
        print("A list of manuals is available using the command `man /`.")
        print("`man` is fully compatible with the `xx` scripting system, and is used for documenting complex features.")
        print("interactive_help $ ")
        div()
        print("This will be added in Beta 10.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "8":
        div()
        print("Future additions to Files:")
        print("[-] Rename command")
        print("[-] Copy/paste commands")
        print("   [-] Copy data from a file, and paste it into a new/existing file.")
        print("[-] View command fix")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "9":
        print("[-] Standard Library 1.0.0")
        print("[-] Compiler")
        print(f"   [-] Compile any Python script to a {os_name}-compatible package.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "10" or ch == ">":
        future_features_2()
    else:
        if return_mode == 0:
            main()
        else:
            return None
def man(manual, return_mode = 0):
    if manual == "man":
        print("Man is a manual system that allows for programs")
        print("to create manuals that can be displayed to users.")
        div()
        print("In order to use man, here are some tips:")
        div()
        print("[-] To see a list of installed manuals, type MAN / into the terminal.")
        print(f"[-] To see {os_name}'s changelog, type MAN CHANGES.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "stdlib":
        print("The Pythinux standard library adds extra functionality to SZIPS programs, which can be taken advantage of.")
        print("To add SZIPS functionality to a program, add:")
        print("import stdlib")
        div()
        print("To the top of the file.")
        print("Example features:")
        print("[-] Clear screen")
        print("[-] Change terminal colour")
        print("[-] etc.")
        div()
        print("Every Pythinux installation comes with a built-in STDLIB. In order to install it, type INSTALL STDLIB.")
        print("The STDLIB command allows you to test and communicate with the Standard Library.")
        print("Typing stdlib --help shows all STDLIB commands.")
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "install":
        print("Pythinux comes with several programs which are not installed by default. `install` is a command that installs them.")
        print("Type `install <command>` to install <command>, if valid.")
        print("[`install --list` just shows a list]")
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "removed-man":
        div()
        print("Removed manuals:")
        print("rewrite")
        div()
        print("Manuals to be removed by 1.0:")
        print("removed-man todo deprecated future_features")
    elif manual == "deprecated":
        print("Certain programs have been deprecated [scheduled for removal]* or removed.")
        print("This is a list of programs that have been removed since Beta 5 and programs on the way out.")
        div()
        print("DEPRECATED")
        div()
        print("[N/A]")
        div()
        print("REMOVED")
        div()
        print("vim_legacy tens bytegen scriptux files_legacy ping")
        div()
        print("* That is not what deprecated actually means")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "/":
        div()
        print("MANUAL LIST")
        div()
        print("changes deprecated man / removed_man vim echo scripting todo mem updates template szips future_features stdlib alias startup consent")
        div()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "consent":
        div()
        print("Consent mode is a Scripting feature that allows for elevated functions in a script.")
        print("It allows for:")
        print("[-] Running SZIPS programs")
        print("[-] etc.")
        print("Consent mode requires user consent.")
        print("For a guide for it, type `install consent-guide` into the terminal.")
        div()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "alias":
        print("Aliases allow for custom commands.")
        print("An optional file called ALIASES.PYTHINUX contains one alias per line.")
        div()
        print("Format:")
        print("<command_name>|<command>")
        div()
        print("if you type <command_name>, <command> gets executed. Note that built-in commands have priority over aliases.")
        print("Uses:")
        print("[-] Connecting an alias with a script to run that script while looking like a command")
        print("[-] Creating alternate names for commands [for example, turning CLS into CLEAR.")
        print("[-] Downloading files from the Internet with a single command.")
        print("[-] etc.")
        div()
        print("Instructions")
        print("[-] To add an alias, type `add_alias`")
        print("[-] To interact with aliases, type `alias`")
        print("[-] To disable aliases, create a file named .noalias")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "vim":
        div()
        print("Vim is a text editor. It is capable of adding to the end of files.")
        print("While it is basic, it is functional.")
        print("To open it, type VIM.")
        div()
        print("There will be 10 options.")
        div()
        print("Option [1] lets you create or edit files.")
        print("Option [2] lets you view the contents of files.")
        print("Option [3] deletes a file.")
        print("Option [4] opens a file in write mode, not append mode.")
        print("Options [5],[6] and [8] pertain to backups of VIMX files.")
        print("OPtions [7] and [9] pertain to the now-deprecated legacy Vim.")
        print("Option [10] presents you with a nice list of all files in the current directory.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "changes":
        div()
        print(f"{os_name} v{app_version[0]}.{app_version[1]}.{app_version[2]} changes")
        div()
        print("[-] Added Consent Mode [man consent]")
        print("[-] Fixed bug where aliases break user login")
        print("[-] Added MEM system.")
        print("[-] Added Setup Wizard [currently optional and incomplete")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "echo":
        print(f"In the old {os_name}, you could use functionality in Echo that has not been ported over.")
        print("The functionality allowed for the quick creation of files and the echoing of variable data.")
        div()
        print("This functionality will be added soon.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "scripting" or manual == "xx":
        div()
        print(f"The scripting system is a new system in {os_name} that allows you to run terminal commands, one at a time.")
        div()
        print("The Concept")
        div()
        print("It is basically the same as Bash in Linux or Batch in Windows. It allows you to run multiple commands at once, automatically, aithout needing to type them out.")
        print("Scripts end in .xx and are in plaintext.")
        div()
        print("Creating a Script")
        div()
        print("[-] Create a new .XX file [In files, do \"vim <filename>.xx\"]")
        print("[-] On each line, enter each command you'd like to run, in the same way as you would type it normally.")
        div()
        print("Running a Script")
        div()
        print("To run a script, type ./[script name]. Replace [script name] with the file name of the XX file. Do not put \".xx\" at the end.")
        div()
        print("Script-Exclusive Stuff")
        div()
        print("[-] div() places a div() element on the screen")
        print("[-] Timer does not show a number in scripts")
        print("[-] Syntax Errors hidden ins scripts.")
        print("[-] cmd [command] sends a command to the host OS's default terminal")
        div()
        print("Status & Limitations")
        div()
        print("The script system is fully experimental, but it will be added to, and new features will have it in mind.")
        print("It is not guaranteed to work, and a lot of commands do not support it.")
        div()
        print("Tips")
        div()
        print("[-] Use echo to print text to the screen")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "custom_manual" or manual =="cman":
        main("cls")
        div()
        print("By 1.0, there will be a Custom Manual System with a full file format.")
        print("For a demo, type `install cman_demo`.")
        div()
        print("Idea")
        div()
        print("A .cman file can be added to the current folder, containing everything in the manual.")
        print("Typing cman / shows every single .cman file in the current directory.")
        print("To choose a man, type cman <manual>.")
        div()
        print("Uses")
        div()
        print("Programs can use CMAN in order to create manuals in a way that is easy to maintain yet still works 100% of the time.")
        print("A program can have a help utility that has easy-to-edit, portable manuals.")
        div()
        print("Name")
        div()
        print("Yes, I am aware. I don't have a better name.")
        div()
        print("Challenges")
        div()
        print("[-] File Format")
        print("[-] Folder Support")
        print("[-] Version identification")
        print("   [-] Could use separate file formats")
        print("[-] etc.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "todo":
        div()
        print("[-] All future features [MAN FUTURE_FEATURES}")
        print("[-] Complete User Control")
        print("[-] Proper documentation for every command")
        print("[-] Finish STARTED command")
        print("[-] Finish scripting system [MAN TODO_SCRIPTS]")
        print("[-] Full Mem Support")
        print("[-] Custom Manual System [man custom_manual]")
        div()
        print("MAN TODO_SCRIPTS")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "todo_scripts":
        div()
        print("[-] MEM integration")
        print("[-] File operations")
        print("[-] Consent Mode")
        print("   [-] Enable to allow for extra features")
        print("   [-] User required to allow for it to be turned on")
        print("[-] Direct Python execution")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "mem":
        main("cls")
        div()
        print("MEM is a memory system similar to that of a calculator's M function.")
        div()
        print("MEM Value")
        div()
        print(f"The value of MEM is stored in {os_name}'s memory.")
        print("To view MEM's current value, type `mem --view` or `mem -v`.")
        print("To set it, type `mem --set <value>`, replacing <value> with a number.")
        print("To clear it, type `mem --reset` or `mem -r`.")
        div()
        print("Addition and Subtraction")
        div()
        print("To add a certain value to MEM, type `mem --add <value>`")
        print("To subrtact a certain value to MEM, type `mem --add <value>`")
        div()
        print("Backup/Restore")
        div()
        print("To save MEM to a file, type `mem --backup` or `mem -b`. It will save to a file.")
        print("To restore from the backup, type `mem --restore` or `mem -rs`. It will load the backup.")
        br()
        main()
    elif manual == "updates":
        print(f"{os_name} updates are regularly released. While there is no schedule, they do add features and security improvements.")
        print(f"Current version: v{app_version[0]}.{app_version[1]}.{app_version[2]}")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "template":
        div()
        print(f"Template is a small command that creates files that you can use when writing programs for {os_name}.")
        print("template - create a file called template.zip which contains program.py, which is loaded when SZIPS opens a program.")
        print("template -p - creates a file called template.py, which can be edited and used for SZIPS.")
        print("template -d - Finds and deletes the following files in the current directory:")
        print("[-] template.zip")
        print("[-] template.py")
        print("[-] program.py")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "future_features":
        future_features()
    elif manual == "szips":
        print(f"SZIPS [Super Zipped Internal Program System] allows for the execution of Python code in {os_name}.")
        print(f"This manual serves as a guide for how to create and execute programs in {os_name}.")
        print("1 Linux Guide")
        print("[-] Enter TEMPLATE -P into the terminal")
        print("[-] enter TERMINAL into the terminal")
        print("[-] Enter \"nano template.py\" into the terminal")
        print("[-] Using GNU Nano, create your program.")
        print("[-] Once you're done, press CTRL+X to exit. Presss Y to save if prompted.")
        print(f"[-] Once you are back in the terminal, type %%exit to return to {os_name}.")
        print("[-] Type \"build-prog template.py\" to compile the program to a ZIP file.")
        print("[-] Enter the name of the ZIP file.")
        print("2 Windows Guide")
        print("[-] Enter TEMPLATE -P into the terminal")
        print("[-] enter IDLE-LAUNCH into the terminal")
        print("[-] IDLE, the Python IDE, will open. Press CTRL+O and open TEMPLATE.PY in the current directory.")
        print("[-] Write your program. Once you're done, save and close IDLE.")
        print("[-] Type \"build-prog template.py\" to compile the program to a ZIP file.")
        print("[-] Enter the name of the ZIP file.")
        print("3 Running")
        print("[-] Type RUN into the terminal.")
        print("[-] Enter the name of the program's ZIP file. It will then run.")
        print("4 Basic Tips")
        print("[-] Once you've finished compiling, type TEMPLATE -D to clean up.")
        br()
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "cmde":
        print("CMD -E <command>")
        print("Works like bash or batch, you type the name of a file and it runs every line of the file through the OS's default terminal.")
        if return_mode == 0:
            main()
        else:
            return None
    elif manual == "startup":
        print("If you reate a file called .startup in the same directory as your {os_name} folder, the contents of it will be run by Pythinux, like a script run on startup. Unlike a script, you can run ./ scripts.")
    elif manual == "stdlib_internal":
        if is_stdlib() == True:
            stdlib.help()
        else:
            print("Standard Library not installed.")
        if return_mode == 0:
            main()
        else:
            return None
    else:
        return True
def files(startpoint,start=0,safemode=0):
    if start == 1:
        div()
        print("Files")
        div()
        print("For help, type HELP.")
        div()
        print("Files is a command-line file explorer.")
        print("It is similar to CMD in Windows.")
        if safemode == 1:
            print("Safe mode is on. Certain commands do not work.")
        div()
    prompt = input(f"{os.getcwd()} />")
    if prompt == "help":
        div()
        print("Command list + description")
        div()
        print("help = Gives you help")
        print("cd <dir> = changes to another directory")
        print("exit = Closes Files.")
        if safemode == 0:
            print("mark = Set current directory as Startpoint.")
        print("startpoint = Change current directory to Startpoint.")
        if safemode == 0:
            print("safemode = enables safe mode [certain commands disabled] [cannot disable]")
        if safemode == 0:
            print("clear = clear a file's contents")
        print("dir = List all files and fodlers in current directory")
        print("dir /w = Lists all folders in current directory")
        if safemode == 0:
            print("md <folder> = Create a folder named <folder>")
            print(f"del <file> = Delete <file>")
            print(f"create <file> = Creates a blank file named <file>")
        print("view <file> = Prints contents of <file>")
        print("cls = clears screen")
        print("ver = prints files version")
        if safemode == 0:
            print("vim <file> = Opens file in Vim")
        br()
        files(startpoint,0,safemode)
    elif prompt == "exit":
        os.chdir(startpoint)
        main()
    elif prompt == "cls":
        clear_screen()
        files(startpoint,0,safemode)
    elif prompt == "safemode" and safemode == 0:
        files(startpoint,1,1)
    elif prompt == "ver":
        if type(app_version[2]) == str:
            print(f"files 1.1.0 @ {os_name.lower()} {app_version[0]}.{app_version[1]}.{app_version[2].lower()}")
        else:
            print(f"files 1.1.0 @ {os_name.lower()} {app_version[0]}.{app_version[1]}.{app_version[2]}")
        files(startpoint,0,safemode)
    elif "cd " in prompt:
        try:
            os.chdir(prompt[3:])
        except:
            pass
        files(startpoint,0,safemode)
    elif prompt == "cd..":
        os.chdir("..")
        files(startpoint,0,safemode)
    elif prompt == "startpoint":
        os.chdir(startpoint)
        files(startpoint,0,safemode)
    elif prompt == "":
        files(startpoint,0,safemode)
    elif prompt == "mark" and safemode == 0:
        files(os.getcwd())
    elif "clear " in prompt  and safemode == 0:
        try:
            f = open(prompt[6:],"w")
            f.close()
            print("Successfully cleared file.")
        except:
            print("Failed to clear file.")
        print(startpoint)
        files(startpoint,0,safemode)
    elif prompt == "dir" or prompt == "ls":
        dirname=os.getcwd()
        filee = os.listdir(dirname)
        for file in filee:
            print(file)
        files(startpoint,0,safemode)
    elif "view " in prompt:
        try:
            f=open(prompt[5:],"r")
            data=f.read()
            f.close()
            data=data.split("\n")
            for item in data:
                print(item)
            br()
            files(startpoint,0,safemode)
        except:
            files(startpoint,0,safemode)
    elif prompt == "dir /w" or prompt == "dir/w" or prompt == "dir /q" or prompt == "dir/q":
        dirname=os.getcwd()
        filee = os.listdir(dirname)
        for file in filee:
            if os.path.isdir(file) == True:
                print(file)
        files(startpoint,0,safemode)
    elif "md " in prompt and safemode == 0:
        try:
            os.mkdir(prompt[3:])
        except:
            print("Failed to create directory.")
        files(startpoint,0,safemode)
    elif "del " in prompt and safemode == 0:
        unallowed = [".noalias",".no_autologin"]
        for item in unallowed:
            if item == prompt[4]:
                ch="del "
        try:
            os.remove(prompt[4:])
        except:
            print("Could not remove file.")
        files(startpoint,0,safemode)
    elif "create " in prompt and safemode == 0:
        try:
            f=open(prompt[7:],"w")
            f.close()
        except:
            print("Could not open file.")
        files(startpoint,0,safemode)
    elif prompt == "safemode" and safemode == 1:
        print("Safe mode cannot be disabled. Exit Files and re-enter it to disable it, if you have the priveleges to run Files without safe mode.")
        files(startpoint,0,1)
    elif "vim " in prompt and safemode == 0:
       vim_editor(prompt[4:]) 
    else:
        print(f"{upper(prompt)} IS NOT A VALID COMMAND OR DIRECTORY.")
        files(startpoint,0,safemode)
def remove_userlist():
    # https://www.geeksforgeeks.org/python-os-remove-method/
    import os
    # File name
    file = 'userlist.pythinux'
    # File location
    location = str(os.getcwd())
    # Path
    path = os.path.join(location, file)
    # Remove the file
    # 'file.txt'
    os.remove(path)
    refresh_data()
    login()
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
        print(f"The fatal error occured and {os_name} was forced to terminate itself in order to protect the hardware and software from irreversible damage.")
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
        print(f"The fatal error occured and {os_name} was forced to terminate itself in order to protect the hardware and software from irreversible damage.")
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
def auth(msg="AUTHENTICATION"):
    div()
    print(msg)
    div()
    global password
    newpass=getpass.getpass("Password $")
    if password == newpass or password == sha256(newpass):
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
    elif user_lvl == 1:
        print("In order to perform this function, you need to enter your password.")
        if auth() == True:
            return True
        else:
            return False
    else:
        return False
def is_root_rigid():
    # The old version of is_root(). Current is_root() allows for standard users to access root-only programs. This one does not.
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
def is_stdlib():
    try:
        data=stdlib
        return True
    except:
        return False
def lower(inp):
    if isinstance(inp,str) == True:
        return inp.lower()
    else:
        return "[UNDEFINED]"
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
def user_control():
    div()
    print("[0] Return")
    print("[x] User List")
    print("[x] User Remove")
    print("[x] Edit User Details")
    print("[4] Refresh Userlist Data")
    print("[5] Force Disable Autologin")
    print("[6] Undo #5")
    print("[7] Set Autologin Details")
    div()
    try:
        ch=int(input(">"))
    except:
        user_control()
    if ch == 4:
        refresh_data()
        div()
        print("Refreshed user list.")
        user_control()
    elif ch == 5:
        try:
            f=open(".no_autologin","w")
            f.close()
            div()
            print("Action completed successfully.")
        except:
            div()
            print("Failed to complete action.")
        user_control()
    elif ch == 6:
        try:
            os.remove(".no_autologin")
            div()
            print("Action completed successfully.")
        except:
            div()
            print("Failed to complete action.")
        user_control()
    elif ch == 7:
        try:
            f=open(".autologin","w")
            un=input("Username >>")
            un=un.replace("|","")
            pw=getpass.getpass("Password >>")
            f.write(f"{un}|{pw}")
            f.close()
            div()
            print("Completed action successfully.")
            print("Login username:",un)
        except:
            div()
            print("Failed to complete action.")
        user_control()
    else:
        main()
    main()
def setup_wizard():
    div()
    print(f"{os_name} Setup Wizard")
    div()
    print(f"Welcome to {os_name}. This setup wizard will allow you to setup your {os_name} system for use.")
    print(f"Firstly, enter a username for your MAIN account:")
    un_main=""
    while len(un_main) == 0:
        un_main=input(">")
        if len(un_main) == 0:
            print("Must enter a username. Try again.")
    print("Secondly, type a password for that account.")
    pass_main=""
    while len(pass_main) == 0:
        pass_main=getpass.getpass(">")
        if len(pass_main) == 0:
            print("Must enter a password. Try again.")
    pass_main=sha256(pass_main)            
    print("Next, do you want to add an admin account for controlling the network?")
    print("[1] Yes")
    print("[0] No")
    try:
        ch=int(input(">"))
    except:
        ch = 0
    if ch == 1:
        is_admin=1
        admin_un=""
        while len(admin_un)==0:
            admin_un=input("Admin Username >>")
        admin_pass=""
        while len(admin_pass) == 0:
            admin_pass=getpass.getpass("Admin Password >>")
        admin_pass = sha256(admin_pass)
    else:
        is_admin = 0
    stre=f"{un_main}|{pass_main}|1/"
    if is_admin == 1:
        stre += f"{admin_un}|{admin_pass}|2/"
    f=open("userlist.pythinux","w")
    f.write(stre)
    f.close()
    print("Saved users.")
    print(f"You will now be logged off. Log in using your details in order to access {os_name}")
    br()
    main("cls")
    refresh_data()
    login()
def run_script(things):
    if isinstance(things,list) == False:
        things=things.split("\n")
    for item in things:
        if "<input>" in item:
            item = item.replace("<input>",input())
        if "<input2>" in item:
            item = item.replace("<input2>",input())
        if "<input3>" in item:
            item = item.replace("<input3>",input())
        if "<input4>" in item:
            item = item.replace("<input4>",input())
        if "<input5>" in item:
            item = item.replace("<input5>",input())
        main(item)
def main(ch="",allow_script=0):
    global username, password, user_lvl, user_type, data, stdlib, mem, bmem
    if ch == "":
        return_mode = 0
        ch=input(f"{user_type}@{username} $")
    else:
        return_mode = 1
    if ch == "help":
        div()
        print(f"Command List")
        div()
        print(f"about help logoff author mul rand rng time cls")
        print(f"echo started div add sub stopwatch timer getdetails chkroot")
        print(f"quit forgot power sysinfo mod userlist timeloop sqrt area add_user")
        print(f"admin_panel man userlist_c vim run cat update terminal template build-prog")
        print(f"idle-launch jit install stdlib alias add_alias user_control")
        print("setupwizard mem")
        div()
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "jit" and return_mode == 0:
        print("JIT [COMMAND]")
        print("Sends [command] to main().")
        main()
    elif "jit " in ch:
        main(ch[4:])
        main()
    elif ch == "about -c":
        print(f"{os_name} v{app_version[0]}.{app_version[1]}.{app_version[2]}")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "is_stdlib":
        print(is_stdlib())
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "about":
        div()
        print(f"{upper(os_name)} v{app_version[0]}.{app_version[1]}.{app_version[2]}")
        div()
        print(f"{os_name} is (c) 2022 WinFan3672, some rights reserved.")
        print(f"{os_name} is distributed under the MIT license, a flexible license\nthat gives full control over source code and no warranty.")
        div()
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "logoff":
        login()
    elif ch == "author":
        div()
        print(f"{os_name} was written by WinFan3672.")
        print(f"WinFan3672 is a British developer making stupid things like this.")
        div()
        if return_mode == 0:
            main()
        else:
            return True
    elif ch.replace(" ","") == "":
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "mul":
        print("Syntax:")
        print("mul [int] [int]")
        if return_mode == 0:
            main()
        else:
            return True
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
            if return_mode == 0:
                main()
            else:
                return True
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "time":
        print(strftime("%x %X"))
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "rand":
        print(rng(100000,1000000))
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "rng":
        print("RNG generates a random number from [1st parameter] to [2nd parameter]")
        div()
        print("Correct syntax:")
        print("rng [int] [int]")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch.startswith("rng ") == True:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                print(rng(int(ch[1]),int(ch[2])))
            except:
                print("Only INT numbers are accepted.")
                if return_mode == 0:
                    main()
                else:
                    return True
        else:
            base=[]
            for item in ch:
                if item != "":
                    base.append(item)
            ch=base
            print(f"RNG requires [2] parameters, got [{len(ch)-1}].")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "cls":
        clear_screen()
        if return_mode == 0:
            main()
        else:
            return True
    elif "echo " in ch:
        ch=ch.replace("$date",stime("%x"))
        ch=ch.replace("$time",stime("%X"))
        ch=ch.replace("$user",username)
        ch=ch.replace("$uuser",username.upper())
        ch=ch.replace("$os",os_name)
        ch=ch.replace("$version",f"{app_version[0]}.{app_version[1]}.{app_version[2]}")
        if " > " in ch:
            ch=ch[5:]
            ch=ch.split(" > ")
            if len(ch) == 2:
                f=open(ch[1],"w")
                f.write(ch[0])
                f.close()
                if return_mode == 0:
                    main()
                else:
                    return True
            else:
                print(ch)
                if return_mode == 0:
                    main()
                else:
                    return True
        else:
            print(ch[5:])
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "echo":
        print("echo <str>")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "setupwizard" and return_mode == 0:
        setup_wizard()
    elif ch == "started":
        div()
        print("GETTING STARTED GUIDE")
        div()
        print("In order to enter a list of commands, type HELP.")
        print("In order to log off, type LOGOFF.")
        div()
        print(f"{os_name} has a buit-in help system known as man.")
        print(f"In order to use it, type `man man` for help on how to use it, and `man /` for a list of pre-installed manuals.")
        div()
        print(f"For a noob getting started guide, type `started -n`.")
        print(f"For a non-noob getting started guide, type `started -e`")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "div":
        print("Correct syntax:")
        print("div [int] [int]")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch.startswith("div "):
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
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "add":
        print("Correct syntax:")
        print("add [int] [int]")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch.startswith("add "):
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
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "sub":
        print("Correct syntax:")
        print("sub [int] [int]")
        main()
    elif ch.startswith("sub "):
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
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "timer":
        print("Correct syntax:")
        print("timer [seconds(int)]")
        if return_mode == 0:
            main()
        else:
            return True
    elif "timer " in ch:
        ch=int(ch[6:])
        while ch > 0:
            if return_mode == 0:
                print(ch)
            sleep(1)
            ch -= 1
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "stopwatch":
        print("[Press CTRL+C To Exit]")
        i = 1
        try:
            while True:
                print(i)
                i += 1
                sleep(1)
        except:
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "getdetails":
        if is_root() == True:
            print(f"Username: {username}")
            newpass=""
            for item in password:
                newpass+="*"
            print(f"Password: {newpass}")
            if return_mode == 0:
                main()
            else:
                return True
        else:
            print("You need to be root to access this command.")
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "chkroot":
        print(is_root())
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "quit" or ch == "exit" and return_mode == 0:
        if return_mode == 0:
            exit()
        else:
            main()
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
        if return_mode == 0:
            main()
        else:
            return True
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
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "debug" or ch == "root" and return_mode == 0:
        if is_root_rigid() == True and auth() == True:
            debug_menu()
        else:
            div()
            print("An error occured:")
            print("[-] You are not a ROOT user")
            print("OR:")
            print("[-] You entered an incorrect password.")
            div()
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "mod":
        div()
        print("mod [num1] [num2]")
        print("Outputs [num] % [num2]")
        if return_mode == 0:
            main()
        else:
            return True
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
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "userlist":
        if is_root() == True and return_mode == 0:
            userlist()
        else:
            print("Only ROOT users can access this menu.")
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "timeloop":
        print("Enter CTRL+C to exit.")
        while True:
            try:
                print(strftime("%x %X"))
                sleep(1)
            except:
                main()
    elif ch == "sqrt":
        print("sqrt [float]")
        print("Does sqare root of [float].")
        if return_mode == 0:
            main()
        else:
            return True
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
    elif ch == "user_control" and is_root() == 1:
        user_control()
    elif ch == "add_user":
        if is_root() == True:
            f=open("userlist.pythinux","r")
            d=f.read()
            f.close()
            f=open("userlist.pythinux","w")
            base1=input("Username $")
            base2=sha256(getpass.getpass("Password $"))
            base3=input("UserLVL  $")
            try:
                if int(base3) > user_lvl:
                    base3 = str(user_lvl)
                    print(f"[To prevent privelege escalation, {os_name} has automatically reduced the user level you chose.]")
            except:
                pass
            f.write(d+f"/{base1}|{base2}|{base3}")
            f.close()
            refresh_data()
            print("Added to userlist.")
            if return_mode == 0:
                main()
            else:
                return True
        else:
            print("You must be a ROOT user to access this.")
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "admin_panel":
        if is_root() == True and return_mode == 0:
            div()
            print("Admin Control Panel")
            div()
            print("[1] Regenerate Userlist And Log Out")
            div()
            try:
                ch=int(input(">"))
            except:
                main()
            div()
            if ch == 1:
                os.remove("userlist.pythinux")
                login()
            else:
                print("Could not remove userlist.")
                main()
        else:
            print("Only ROOT users can do this!")
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "man":
        print("man [manual]")
        print("For manual list, type man /")
        print("For help with man, type man man")
        if return_mode == 0:
            main()
        else:
            return True
    elif "man " in ch:
        man(ch[4:],return_mode)
        if return_mode == 1:
            return None
        print(f"{upper(ch)} IS NOT A VALID COMMAND, PROGRAM OR MANUAL.")
        main()
    elif ch == "userlist_c":
        if is_root() == True:
            div()
            for item in data:
                print(item[0])
            div()
            if return_mode == 0:
                main()
            else:
                return True
        else:
            print("Only ROOT users can use this command.")
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "update" and return_mode == 0:
        if isinstance(app_version[2],str) == True:
            print("Unable to check for updates.")
            main()
        import urllib.request

        url = "http://winfan3672.000webhostapp.com/version_check/pythinux.version"
        print("Checking for updates...")
        print(
            f"Current Version: v{app_version[0]}.{app_version[1]}.{app_version[2]}"
        )
        try:
            urllib.request.urlretrieve(url, "pythinux.version")
        except:
            div()
            print("Failed to check for updates.")
            div()
            print("You could try:")
            print("[-] Checking that you are connected to the Internet.")
            print(
                "[-] Checking that winfan3672.000webhostapp.com is still up, since that is the server that provides the version check information."
            )
            print(
                "[-] Checking that http://winfan3672.000webhostapp.com/version_check/openlife.versio exists, since it may have been deleted."
            )
            print(
                "[-] Checking that your antivirus or firewall is not blocking winfan3672.000webhostapp.com/"
            )
            print("[-] On Windows, deleting your DNS resolver cache.")
            if return_mode == 0:
                main()
            else:
                return True
        f = open("pythinux.version", "r")
        data = f.read()
        data = data.split("|")
        data = [int(data[0]), int(data[1]), int(data[2])]
        not_update_text = f"An update for {os_name} [{data[0]}.{data[1]}.{data[2]}] is available.\nNo download available"
        if data[0] > app_version[0]:
            print(not_update_text)
        else:
            if data[1] > app_version[1]:
                print(not_update_text)
            else:
                if data[2] > app_version[2]:
                    print(not_update_text)
                else:
                    print(f"You are on the latest version of {os_name}.")
        if return_mode == 0:
            main()
        else:
            return True
    elif "vim " in ch:
        vim(ch[4:])
    elif ch == "vim" and return_mode == 0:
        div()
        vim()
    elif ch == "files" and return_mode == 0:
        if is_root() == True:
            files(os.getcwd(),1)
        else:
            files(os.getcwd(),1,1)
    elif ch.startswith("run ") and return_mode == 0:
        prog=ch[4:]
        try:
            os.remove("program.py")
        except:
            pass
        if ".zip" not in prog:
            prog+=".zip"
        try:
            import sys
            sys.path.insert(0,prog)
            import program
            program.p_start()
            del(program)
            main()
        except:
            main()
    elif ch == "run" and return_mode == 0:
        try:
            os.remove("program.py")
        except:
            pass
        prog=input(">>")
        if ".zip" not in prog:
            prog+=".zip"
        try:
            import sys
            sys.path.insert(0,prog)
            import program
            program.p_start()
            del(program)
            main()
        except:
            main()
    elif ch == "./" and return_mode == 0:
        print("./[name of .xx file]")
        print("For instructions, type MAN SCRIPTING or MAN XX")
        main()
    elif "./" in ch and return_mode == 0 or allow_script == 1:
        consent_mode = 0
        try:
            f=open(ch[2:]+".xx","r")
            data=f.read()
            f.close()
            run_script(data.split("\n"))
            consent_mode = 0
            main()
        except:
            print("Could not run script.")
            consent_mode = 0
            main()
    elif ch == "div()" and return_mode == 1:
        div()
        return True
    elif ch == "cat" and return_mode == 0:
        print("CAT [url] [filename]")
        print("Downloads [url] and saves it to [filename]")
        main()
    elif "cat " in ch:
        ch=ch.split(" ")
        if len(ch) == 3:
            try:
                import urllib.request
                url = ch[1]
                saveas=ch[2]
                print("Downloading...")
                try:
                    urllib.request.urlretrieve(url, saveas)
                    print("Downloaded.")
                except:
                    raise Exception
            except:
                print("FAILED.")
        else:
            if return_mode == 0:
                print("Invalid parameters.")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "terminal" and return_mode == 0:
        print("To exit the TERMINAL, type %%exit")
        terminal()
    elif "cmd -e " in ch:
        try:
            f=open(ch[7:],"r")
            data=f.read()
            f.close()
            data=data.split("\n")
            for item in data:
                os.system(item)
        except:
            print("Failed to run script.")
        main()
    elif "cmd " in ch and return_mode == 1:
        os.system(ch[4:])
        return True
    elif ch == "template -d":
        if is_root() == True:
            try:
                os.remove("program.py")
            except:
                pass
            try:
                os.remove("template.py")
            except:
                pass
            try:
                os.remove("template.zip")
            except:
                pass
            print("Operation completed successfully.")
            main()
        else:
            print("Insufficient priveleges- only ROOT users can access.")
            main()
    elif ch == "stdlib" and return_mode == 0:
        div()
        print(f"STDLIB Installed: {is_stdlib()}")
        if is_stdlib() == True:
            print(f"Version: {stdlib.app_version_str}")
        if is_stdlib == False:
            print("To install Standard Library, type INSTALL STDLIB")
        div()
        print("STDLIB --HELP for help")
        main()
    elif ch == "stdlib --help" and return_mode == 0:
        print("STDLIB <parameter>")
        print("<only supports 1 parameter at a time")
        print("Valid parameters:")
        print("--help = Displays help")
        print("--help-stdlib = Shows stdlib.help()")
        print("--console = Opens STDLIB console")
        print("--install = Installs STDLIB from stdlib.py")
        print("--remove = Uninstalls Standard library")
        main()
    elif ch == "stdlib --help-stdlib" and return_mode == 0:
        if is_stdlib() == True:
            main("cls")
            stdlib.help()
            main()
        else:
            print("Standard Library not installed.")
            main()
    elif ch == "stdlib --install" and return_mode == 0:
        try:
            try:
                del(stdlib)
            except:
                pass
            import stdlib
            print("Installed successfully.")
            print(f"Version: {stdlib.app_version_str}")
        except:
            print("Could not install Standard library.")
        main()
    elif ch == "install consent_guide" and return_mode == 0:
        div()
        print("Consent Mode Guide")
        div()
        print("In a script, certain functions are disallowed for security reasons.")
        print("However, there may be genuine reasons for using said functions.")
        print("This is where Consent Mode comes in.")
        print("In a `xx` script, you can call `consent_mode` and a Consent Mode screen will appear.")
        div()
        print("#Example script")
        print("echo This is now the script")
        print("consent_mode")
        div()
        print("If you run the code, a Consent Mode message appears, asking the user to type `YES` in order to allow for extended functionality.")
        print("In order to prevent breaking your program, `consent_check` can be called. If no consent is given, an error is thrown and the script ends.")
        print("To revoke consent, call `revoke_consent`. This is automatically done when the script ends.")
        br()        
        main()
    elif ch == "install numpy":
        try:
            import numpy
            print("Numpy already installed.")
            if return_mode == 0:
                main()
            else:
                return True
        except:
            os.system("pip install numpy")
            os.system("pip3 install numpy")
            try:
                import numpy
                del(numpy)
                print("Successfully installed numpy.")
            except:
                print("Failed to install numpy.")
            if return_mode == 0:
                main()
            else:
                return True
    elif ch == "install cman_demo":
        print("Custom Manual Demo")
        print("Command list: help")
        print("To exit: return")
        cman_demo()
    elif ch == "install" and return_mode == 0:
        print("install <program>")
        print("Installs <program> and imports it.")
        div()
        print("Valid programs:")
        print("stdlib numpy cman_demo")
        main()
    elif ch == "install --help" and return_mode == 0:
        print("install <program> OR install <parameter>")
        print("For a list of installable programs, type install --list.")
        div()
        print("Parameters [Use one at a time]:")
        print("--help = Shows this menu")
        print("--list = Lists all installable programs")
        main()
    elif ch == "install --list" and return_mode == 0:
        print("stdlib numpy")
        main()
    elif ch == "stdlib --remove" and return_mode == 0:
        try:
            del(stdlib)
        except:
            pass
        main()
    elif ch == "stdlib --console" and return_mode == 0:
        install_stdlib()
        print("Type %%exit to exit STDLIB console")
        while True:
            ch=input(">")
            if ch == "%%exit":
                break
            stdlib.console(ch)
        main()
    elif ch == "cls -s":
        install_stdlib()
        stdlib.cls()
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "template -p":
        print("Created file called PROGRAM.PY.")
        print("Open it and edit it.")
        f=open("program.py","wb")
        import base64
        f.write(base64.b64decode("'ZGVmIHBfc3RhcnQoKToNCiAgICAjIEluc2VydCBhbGwgb2YgeW91ciBjb2RlIGJlbG93IHRoaXMgbGluZSENCg=='"))
        f.close()
        main()
    elif ch == "install stdlib":
        print("Installing Standard Library v0.0.1...")
        import base64
        f=open("stdlib.py","wb")
        f.write(base64.b64decode("'aW1wb3J0IG9zDQpmcm9tIHBsYXRmb3JtIGltcG9ydCB1bmFtZQ0KaW1wb3J0IGJhc2U2NA0KYXBwX3ZlcnNpb24gPSBbMCwwLDFdDQphcHBfdmVyc2lvbl9zdHIgPSAiMC4wLjEiDQoNCiMgUHl0aGludXggU3RhbmRhcmQgTGlicmFyeQ0KZGVmIGhlbHAoKToNCiAgICBwcmludCgiVGhlIFB5dGhpbnV4IFN0YW5kYXJkIExpYnJhcnkgYWxsb3dzIHlvdSB0byBhY2Nlc3MgY29vbCBBUEkgc3R1ZmYuXG4iKQ0KICAgIHByaW50KCIxIEltcGxlbWVudGluZyBJbiBQcm9ncmFtIikNCiAgICBwcmludCgiSW4gb3JkZXIgdG8gYWRkIHRoZSBTVERMSUIgaW50byB5b3VyIHByb2dyYW0sIHBsYWNlIHRoZSBmb2xsb3dpbmcgbGluZSBhdCB0aGUgdG9wIG9mIHlvdXIgY29kZToiKQ0KICAgIHByaW50KCJcbmltcG9ydCBzdGRsaWIiKQ0KICAgIHByaW50KCJcblRoaXMgd2lsbCBhbGxvdyB5b3UgdG8gYWNjZXNzIGV2ZXJ5IGZ1bmN0aW9uIG9mIHN0ZGxpYi4iKQ0KZGVmIHZlcnNpb25fY2hlY2sodmVyLGlzX3N0cj0xKToNCiAgICAjIElmIGlzX3N0ciA9IDAgaXQgY2hlY2tzIGFnYWluc3QgYXBwX3ZlcnNpb24sIGlmIDEgaXQgY2hlY2tzIGFnYWluc3QgYXBwX3ZlcnNpb25fc3RyICAgIA0KICAgIGlmIGlzX3N0ciA9PSAwIGFuZCB2ZXIgPT0gYXBwX3ZlcnNpb246DQogICAgICAgIHJldHVybiBUcnVlDQogICAgZWxpZiBpc19zdHIgPT0gMSBhbmQgdmVyID09IGFwcF92ZXJzaW9uX3N0cjoNCiAgICAgICAgcmV0dXJuIFRydWUNCiAgICBlbHNlOg0KICAgICAgICByZXR1cm4gRmFsc2UNCmRlZiBjbHMoKToNCiAgICByZXM9dW5hbWUoKQ0KICAgIG9zLnN5c3RlbSgiY2xzIiBpZiByZXNbMF0gPT0gIldpbmRvd3MiIGVsc2UgImNsZWFyIikNCmRlZiBjb25zb2xlKGNtZCk6DQogICAgaWYgY21kID09ICJoZWxwIjoNCiAgICAgICAgcHJpbnQoImhlbHAgPSB0aGlzIG1lbnUiKQ0KICAgICAgICBwcmludCgiY2xzID0gY2xzKCkiKQ0KICAgICAgICBwcmludCgiaGVscCAtLXN0ZGxpYiA9IGhlbHAoKSIpDQogICAgICAgIHByaW50KCJnZmQgPGZpbGVuYW1lPiA9IFByaW50IGZpbGUgZGF0YSBvZiA8ZmlsZW5hbWU+IikNCiAgICAgICAgcmV0dXJuIE5vbmUNCiAgICBlbGlmIGNtZCA9PSAiY2xzIjoNCiAgICAgICAgY2xzKCkNCiAgICBlbGlmIGNtZC5zdGFydHN3aXRoKCJnZmQgIik6DQogICAgICAgIHByaW50KGdldF9maWxlX2RhdGEoY21kWzQ6XSkpDQogICAgZWxpZiBjbWQgPT0gImhlbHAgLS1zdGRsaWIiOg0KICAgICAgICBoZWxwKCkNCmRlZiBnZXRfZmlsZV9kYXRhKGZuLG1vZGU9InIiKToNCiAgICB0cnk6DQogICAgICAgIGY9b3Blbihmbixtb2RlKQ0KICAgICAgICBkYXRhPWYucmVhZCgpDQogICAgICAgIGYuY2xvc2UoKQ0KICAgICAgICByZXR1cm4gZGF0YQ0KICAgIGV4Y2VwdDoNCiAgICAgICAgcmV0dXJuIE5vbmUNCmRlZiBiNjRlKGRhdGEpOg0KICAgIHJldHVybiBiYXNlNjQuYjY0ZW5jb2RlKGRhdGEpLmRlY29kZSgiYXNjaWkiKQ0KZGVmIGI2NGQoZGF0YSk6DQogICAgcmV0dXJuIGJhc2U2NC5iNjRkZWNvZGUoZGF0YSkNCmRlZiBpc2ZpbGUoZm4pOg0KICAgIHJldHVybiBvcy5wYXRoLmlzZmlsZShmbikNCg=='"))
        f.close()
        install_stdlib()
        print("Successfully installed standard library.")
        if return_mode == 0:
            main()
        else:
            return True
    elif ch == "revoke_consent":
        consent_mode = 0
        if return_mode == 0:
            main()
        else:
            return True
    elif ch.startswith("#") and return_mode == 1:
        return True
    elif ch == "consent_mode" and return_mode == 1:
        print("The current program is asking for elevated priveleges.")
        print("In order to allow these priveleges, type YES [exactly as I put ut]")
        if input("$") == "YES":
            consent_mode = 1
        else:
            consent_mode = 0
            print("Consent not provided.")
        return True
    elif ch == "consent_check" and return_mode == 1:
        print(consent_mode)
        if consent_mode == 1:
            return True
        else:
            print("The program has requested elevated priveleges.")
            print("Due to a lack of elevated priveleges, it cannot run.")
            main()
    elif ch == "template":
        print("Created file called TEMPLATE.ZIP.")
        print("Open it and edit it.")
        print("Note: To create a PROGRAM.PY file instead, type TEMPLATE -P into the shell")
        f=open("template.zip","wb")
        import base64
        f.write(base64.b64decode("UEsDBAoAAAAAAFoAi1WHIBaKgwAAAIMAAAAKAAAAcHJvZ3JhbS5weWRlZiBwX3N0YXJ0KCk6DQogICAgIyBJbnNlcnQgYWxsIG9mIHlvdXIgY29kZSBiZWxvdyB0aGlzIGxpbmUhDQogICAgIyBUbyBlbmQgeW91ciBwcm9ncmFtLCBjYWxsIHBfZW5kKCkNCmRlZiBwX2VuZCgpOg0KICAgIG1haW4oKQ0KUEsBAj8ACgAAAAAAWgCLVYcgFoqDAAAAgwAAAAoAJAAAAAAAAAAgAAAAAAAAAHByb2dyYW0ucHkKACAAAAAAAAEAGAB/+Mjo8wzZAYuLBurzDNkB+4o7xfMM2QFQSwUGAAAAAAEAAQBcAAAAqwAAAAAA"))
        f.close()
        main()
    elif ch == "build-prog":
        print("build-prog [file name]")
        print("Places the file name into an uncompressed ZIP file.")
        print("Used when compiling SZIPS files.")
        main()
    elif ch == "add_alias" and return_mode == 0:
        if os.path.isfile("alias.dat") == False:
            f=open("alias.dat","w")
            f.close()
        f=open("alias.dat","a")
        inp1=input("Alias >>")
        inp1=inp1.replace("|","")
        inp2=input("Command >>")
        inp2=inp2.replace("|","")
        f.write(f"{inp1}|{inp2}\n")
        f.close()
        main()
    elif ch == "alias" and return_mode == 0:
        div()
        print("alias <parameter>")
        print("Only 1 parameter at a time")
        div()
        print("Parameters:")
        print("--list = Lists all aliases")
        print("--list-plus = Lists all aliases and all their respective commands")
        print("--disable = Disables aliases [requires god permission]")
        print("--enable = Re-enables aliases [requires god permission]")
        div()
        print("man alias to learn more about aliases")
        main()
    elif ch == "alias --disable" and return_mode ==0 and is_god() == 1:
        f=open(".noalias","w")
        f.close()
        print("Performed action successfully.")
        main()
    elif ch == "alias --list" and return_mode == 0:
        try:
            f=open("alias.dat","r")
            data=f.read()
            f.close()
            data=data.split("\n")
            data2=[]
            for item in data:
                if item != "":
                    item=item.split("|")
                    data2.append(item[0])
            for item in data2:
                print(item)
            main()
        except:
            print("Could not perform command; Perhaps no aliases exist.")
            main()
    elif ch == "alias --enable" and return_mode == 0 and is_god() == 1:
        try:
            os.remove(".noalias")
        except:
            pass
        print("Action performed successfully.")
        main()
    elif ch == "alias --list-plus" and return_mode == 0:
        try:
            f=open("alias.dat","r")
            data=f.read()
            f.close()
            data=data.split("\n")
            data2=[]
            for item in data:
                try:
                    item=item.split("|")
                    data2.append(f"{item[0]} = {item[1]}")
                except:
                    pass
            for item in data2:
                print(item)
            main()
        except:
            print("Could not perform command; Perhaps no aliases exist.")
            main()    
    elif "build-prog " in ch:
        try:
            ch=ch[11:]
            import zipfile
            zname=input("Zip File Name >>") + ".zip"
            with zipfile.ZipFile(zname, 'a') as myzip:
                myzip.write(ch)
            main()
        except:
            print("Could not compile ZIP file.")
            main()
    elif ch == "idle-launch":
        try:
            import idlelib.idle
            del(idlelib.idle)
            main()
        except:
            print("Could not launch IDLE:")
            print("[-] You do not have a graphics driver installed.")
            print("[-] You are attempting to run Idle more than once. To rectify this, reboot.")
            main()
    elif ch == "mem --help":
        man("mem")
    elif ch == "mem --backup" or ch == "mem -b":
        try:
            f=open("mem.pythinux","w")
            f.write(str(mem))
            f.close()
        except:
            print("Could not save MEM.")
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "mem --restore" or ch == "mem -rs":
        try:
            f=open("mem.pythinux","r")
            mem=float(f.read())
            f.close()
        except:
            print("Could not restore MEM. Does a backup exist?")
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "mem":
        div()
        print("mem <parameter>")
        div()
        print("Parameters")
        div()
        print("--help\n--view -v\n--set\n--reset -r\n--add\n--sub\n--backup -b\n--restore -rs")
        div()
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "mem --view" or ch == "mem -v":
        print(mem)
        if return_mode == 0:
            main()
        else:
            return None
    elif ch.startswith("mem --add ") == True:
        try:
            mem += float(ch[10:])
        except:
            print("Failed to set MEM.")
        if return_mode == 0:
            main()
        else:
            return None
    elif ch.startswith("mem --sub "):
        try:
            mem -= float(ch[10:])
        except:
            print("Failed to set MEM.")
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "mem --set":
        print("mem --set <float>")
        print("sets mem to <float>")
        if return_mode == 0:
            main()
        else:
            return None
    elif ch == "mem --reset" or ch == "mem -r":
        mem=0
        if return_mode == 0:
            main()
        else:
            return None
    elif ch.startswith("mem --set ") == True:
        try:
            mem = float(ch[10:])
        except:
            print("Failed to set.")
        if return_mode == 0:
            main()
        else:
            return None
    else:
        if os.path.isfile(os.getcwd()+"/.noalias") == False and return_mode == 0:
            try:
                f=open("alias.dat","r")
                dat=f.read()
                f.close()
                dat=dat.split("\n")
                data2=[]
                for item in dat:
                    item=item.split("|")
                    data2.append(item)
                dat=data2
                for item in dat:
                    if ch == item[0]:
                        main(item[1])
                        main()
            except:
                pass
        if return_mode == 0:
            print(f"{upper(ch)} IS NOT A VALID COMMAND, PROGRAM, ALIAS, SCRIPT OR MANUAL.")
            if is_stdlib() == False:
                print("NOTE: STANDARD LIBRARY NOT INSTALLED.")
            if os.path.isfile(os.getcwd()+"/.noalias") == True:
                print("NOTE: ALIASES HAVE BEEN DISABLED BY YOUR ADMINISTRATOR.")
        if return_mode == 0:
            main()
        else:
            return True
        
def start(lvl,al):
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
    if al == 0:
        print(f"Welcome to {os_name}.")
        print(f"[{os_name} v{app_version[0]}.{app_version[1]}.{app_version[2]}]")
        div()
        if user_lvl == 0:
            print("You are logged in on a guest account.")
            print("Guest accounts have limited access to commands and cannot run programs.")
        elif user_lvl == 1:
            pass
        elif user_lvl == 2:
            print("You are logged in as a root account.")
            print("If you do not know what this means, type LOGOFF right now.")
            print("DO NOT USE A ROOT ACCOUNT AS YOUR DAILY DRIVER ACCOUNT.")
        elif user_lvl == 3:
            print("Warning! GOD users have very high priveleges and are fully unrestricted.")
            print("Exercise caution and common sense when using a God account.")
            print("If you are unaware of the security implications of using a God account, type LOGOFF right now.")
            print("DO NOT USE A GOD ACCOUNT AS YOUR DAILY DRIVER ACCOUNT.")
    if al == 1:
        main("cls")            
    if user_lvl >= 2:
        if os.path.isfile(os.getcwd()+"/.startup") == True:
            try:
                f=open(".startup","r")
                sdata=f.read()
                f.close()
                sdata=sdata.split("\n")
                for item in sdata:
                    main(item,1)
            except:
                pass
    main()
def login(al=0,al_username="root",al_password="root"):
    global username, password, user_lvl, user_type, autologin, data
    if data == []:
        div()
        print("[Your user file is corrupt. Please delete it.]")
        div()
        data = [["root","root","2"],["user","password","1"],["guest","password","0"]]
    if al == 1:
        base=f"{al_username}:{al_password}"
        sh_base = f"{al_username}:{sha256(al_password)}"
        username,password=f"{al_username}",f"{al_password}"
        autologin = 0
    else:
        div()
        print(f"{upper(os_name)} LOGIN SYSTEM")
        div()
        print("Enter your login details.")
        print("If they are valid, you will be logged in.")
        print(f"There are [{len(data)}] users on your machine.")
        div()
        print("Username = guest\nPassword = password\nFor a guest account")
        div()
        username=input("Username $")
        if username == "//ul":
            l=[]
            for item in data:
                l.append(item[0])
            print(l)
        password=getpass.getpass("Password $")
        div()
        base=f"{username}:{password}"
        sh_base=f"{username}:{sha256(password)}"
    for item in data:
        try:
            if base == f"{item[0]}:{item[1]}":
                start(int(item[2]),al)
            elif sh_base == f"{item[0]}:{item[1]}":
                start(int(item[2]),al)
        except:
            continue
    print("Username or password is invalid.")
    login()
if os.path.isfile(os.getcwd()+"/.no_autologin") == True:
    login(0)
if os.path.isfile(os.getcwd()+"/.autologin") == True:
    f=open(".autologin","r")
    aldata=f.read()
    f.close()
    aldata=aldata.split("|")
    login(1,aldata[0],aldata[1])
login(autologin)
