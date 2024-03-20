import traceback
libconfig = load_program("libconfig", currentUser, libMode=True)

default = libconfig.newConfig()

default.add_section("shell")
default.set("shell", "allowExit", "true")

config = libconfig.loadConfig(default, "shell")
allowExit = config.getboolean("shell", "allowexit", fallback=False)

def run(user, cmd, shell="shell"):
    if cmd == "":
        pass
    elif cmd in ["quit", "exit"] and not allowExit:
        return
    else:
        try:
            runCommand(user, cmd, shell=shell)
        except Exception as e:
            print(traceback.format_exc())


def terminal(user):
    cmd = input("{}@{} $".format(user.group.name, user.username))
    run(user, cmd)
    terminal(user)

def runScript(user, filename):
    with open(filename) as f:
        for cmd in f.read():
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
