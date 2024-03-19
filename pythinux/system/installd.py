import os
import importlib
import zipfile
import traceback
import shutil
import sys

pkm = load_program("pkm silent",currentUser)
def filterDeps(deps):
    filtered_deps = [x for x in deps if x not in pkm.list_app()]
    return filtered_deps, deps
PackageInf = pkm.PackageInf
class InstallerError(Exception):
    def __init__(self,message="Could not install program"):
        self.msg = message
    def __str__(self):
        return self.msg
def installd(path,yesMode=False,depMode=False,upgradeMode=False):
    try:
        with open(path,"rb") as f:
            x = f.read()
        clearTemp()
        os.chdir("tmp")
        with open("program.szip3","wb") as f:
            f.write(x)
        with open("program.szip3","rb") as f:
            with zipfile.ZipFile(f,"r") as zip:
                zip.extractall()
        os.remove("program.szip3")
        if os.path.isfile("program.name"):
            with open("program.name") as f:
                name = f.read()
        else:
            raise InstallerError("No program.name file provided")
        if os.path.isfile("requirements.txt"):
            with open("requirements.txt") as f:
                deps = f.read().split()
                os.chdir("..")
                deps, originalDeps = filterDeps(deps)
                os.chdir("tmp")
        else:
            deps = []
            originalDeps = []
        if os.path.isfile("program.info"):
            with open("program.info") as f:
                info = f.read().split("|")
                for item in info:
                    item.strip()
        else:
            raise InstallerError("No program.info file provided")
        if os.path.isfile("desktop.entry"):
            entryMode=True
        else:
            entryMode=False
        if os.path.isfile("icon.svg"):
            hasIcon = True
        else:
            hasIcon = False
        if os.path.isfile("manuals.zip"):
            manualsMode=True
        else:
            manualsMode=False
        if os.path.isfile("program.py"):
            with open("program.py","rb") as f:
                program = f.read()
        else:
            program = None
        if os.path.isfile("rscript.xx"):
            with open("rscript.xx") as f:
                rscript = f.read()
        else:
            rscript = False
        if os.path.isfile("setup.py"):
            setupMode=True
            with open("setup.py","r") as f:
                setupCode=f.read()
        else:
            setupMode=False
        if os.path.isfile("SYSTEM"):
            system=True
        else:
            system=False
        name = name.replace(" ","")
        name=name.replace("\n","")
        if not yesMode:
            cls()
            div()
            print("Install Program?")
            div()
            print(f"Name: {info[0]}")
            print(f"Version: {info[1]}")
            print(f"Release Date: {info[2]}")
            print(f"Author: {info[3]}")
            print("Dependencies: {}".format("; ".join(deps) if deps else "None"))
            div()
            ch = input("[y/n] $").lower()
        else:
            ch = "y"
        if ch != "y":
            return None
        else:
            os.chdir("..")
            if upgradeMode:
                return info
            try:
                v = info[4]
                v = v.split(".")
                z = []
                for i in v:
                    z.append(int(i))
                v = z
                if v > [version[0],version[1]]:
                    raise InstallerError(f"Package requires newer OS version: {v[0]}.{v[1]}")
            except Exception as e:
                raise InstallerError(str(e))
            dd = "|".join(originalDeps)
            cmd = "pkm register '{}' '{}' '{}' {} '{}' '{}' '{}'".format(name,info[1],dd if originalDeps else [],1 if program else 0,info[0],info[2],info[3])
            load_program(cmd,currentUser,shell="installd")
            no = 1
            for item in deps:
                print(f"({no}/{len(deps)}) Installing '{item}' (dependency of '{name}')...")
                main(currentUser,f"pkm install -d {item}")
                no += 1
            py = sys.executable
            if os.path.isfile("tmp/pip_requirements.txt"):
                ## Install required pip modules
                os.system(f"{py} -m ensurepip")
                os.system(f"{py} -m pip install -r tmp/pip_requirements.txt")
            if setupMode and not yesMode:
                if input("Review setup script? (STRONGLY recommended) [y/n]").lower() == "y":
                    cls()
                    print(setupCode)
                    br()
                print(setupCode)
                exec(setupCode)
            if system:
                fn = f"app_high/{name}.py"
            else:
                fn = f"app/{name}.py"
            if rscript:
                with open(f"rscript/{name}.xx","w") as f:
                    f.write(rscript)
            if program:                
                with open(fn,"wb") as f:
                    f.write(program)
            if entryMode:
                with open("tmp/desktop.entry") as f:
                    entry = f.read()
                with open("icon/{}.entry".format(name)) as f:
                    f.write(entry)
            if hasIcon:
                with open("tmp/icon.svg", "rb") as f:
                    icon_bytes = f.read()
                with open("icon/{}.svg".format(name), "wb") as f:
                    f.write(icon_bytes)
            if manualsMode:
                os.mkdir(f"man/{name}")
                zip_path = os.getcwd()+"/tmp/manuals.zip"
                os.chdir(f"man/{name}")
                with open(zip_path,"rb") as f:
                    with zipfile.ZipFile(f,"r") as zip:
                        zip.extractall()
                os.chdir(cdir)
            if os.path.isfile("tmp/setup.xx"):
                if depMode:
                    silent(lambda:main(currentUser,f"script tmp/setup.xx"))
                else:
                    main(currentUser,f"script tmp/setup.xx")
        if not depMode:
            print(f"Successfully installed '{name}'.")
        else:
            print("Dependency '{}' installed.".format(name))
    except Exception as e:
        print(traceback.format_exc())

def main(arguments):
    if arguments:
        if "-y" in arguments:
            arguments.remove("-y")
            yesMode=True
        else:
            yesMode=False
        if "-d" in arguments:
            arguments.remove("-d")
            yesMode=True
            depMode=True
        else:
            depMode=False
        if "-u" in args:
            args.remove("-u")
            upMode=True
        else:
            upMode=False
        installd(" ".join(arguments),yesMode,depMode,upMode)
    else:
        div()
        print("installd <path/to/installer.szip3>")
        print("Installs an SZIPS3 program.")
        div()
        print("Optional positional arguments:")
        print("    -y: installs without confirmation")
        div()
