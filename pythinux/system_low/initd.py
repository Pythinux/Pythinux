import sys
import traceback
import asyncio

def init(manager):
    async def gc(manager):
        while True:
            manager.garbage_collect()
            await asyncio.sleep(10)

    manager.add_process("gc", lambda: gc(manager))
    manager.run()
    return manager

if args in [["--help"], ["-h"]]:
    div()
    print("initd [args]")
    div()
    print("Positional arguments:")
    div()
    div()
    #print("    --add <command>: add a command to the init file")
    #print("    --view: display the init file")
    #print("    --remove <command>: remove all instances of a command")
    print("    --version: displays the initd version")
    div()
elif args == ["--version"]:
    print("initd 2.0.0-beta2")
else:
    div()
    print("initd is an init system and startup manager.")
    print("It has no user-facing functionality")
    div()
    print("For a command list: initd -h")
    div()
