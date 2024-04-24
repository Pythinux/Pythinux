import traceback

var = load_program("var", currentUser, libMode=True)

def run(user, cmd, lastCommand="", shell="shell",):    
    lastCommandArgs = " ".join(lastCommand.split(" ")[1:])
    if "!!" in cmd:
        cmd = cmd.replace("!!", lastCommand)
    if "!" in cmd:
        cmd = cmd.replace("!", lastCommandArgs)

    if cmd == "":
        pass
    elif cmd in ["quit", "exit"] and not var.getbool("SHELL_ALLOW_EXIT", False):
        pass
    else:
        try:
            runCommand(user, cmd, shell=shell)
        except Exception as e:
            print(traceback.format_exc())


def init(user):
    fileName = "~/shellrc.xx"
    script = file.evalDir(fileName, user)
    runScript(user, script)
    file.changeDirectory("~", user)

def terminal(user, lastCommand=""):
    try:
        cmd = input("[{}@{} {}] $".format(user.group.name, user.username, CURRDIR))
    except KeyboardInterrupt:
        print()
        terminal(user, lastCommand)
    try:
        run(user, cmd, lastCommand)
    except KeyboardInterrupt:
        pass
    if ["!"] in cmd.split(" "):
        terminal(user, lastCommand)
    else:
        terminal(user, str(cmd))

def runScript(user, filename):
    with file.open(filename, user) as f:
        for cmd in [x for x in f.read().split("\n") if not x.startswith(";")]:
            run(user, cmd, "script")
def main(args):
    if args:
        for arg in args:
            runScript(currentUser, arg)
    else:
        div()
        print("shell <script_name.xx>")
        div()
        print("Runs a shell script.")
        div()
