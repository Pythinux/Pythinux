import traceback

var = load_program("var", currentUser, libMode=True)

allowExit = var.getbool("SHELL_ALLOW_EXIT", False)

def run(user, cmd, lastCommand="", shell="shell",):
    
    lastCommandArgs = " ".join(lastCommand.split(" ")[1:])
    if "!!" in cmd:
        cmd = cmd.replace("!!", lastCommand)
    if "!" in cmd:
        cmd = cmd.replace("!", lastCommandArgs)

    if cmd == "":
        pass
    elif cmd in ["quit", "exit"] and not allowExit:
        print("ERROR: Exiting has been disabled.")
    else:
        try:
            runCommand(user, cmd, shell=shell)
        except Exception as e:
            print(traceback.format_exc())


def init(user):
    fileName = "~/shellrc.xx"
    script = file.evalDir(fileName, user)
    runScript(user, script)

def terminal(user, lastCommand=""):
    cmd = input("[{}@{} {}] $".format(user.group.name, user.username, CURRDIR))
    run(user, cmd, lastCommand)
    if ["!"] in cmd.split(" "):
        terminal(user, lastCommand)
    else:
        terminal(user, str(cmd))

def runScript(user, filename):
    with open(filename) as f:
        for cmd in f.read().split("\n"):
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
