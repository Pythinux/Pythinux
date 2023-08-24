import pickle
import urllib.request

global db, dbs, VERSION
db = {}
dbs = {}
VERSION = [3,2,0]

def removeProgram(program):
    if os.path.exists(f"app/{program}.py"):
        os.remove(f"app/{program}.py")
    elif os.path.exists(f"app_high/{program}.py"):
        os.remove(f"app_high/{program}.py")
    else:
        pass
    print(f"Successfully removed {program}.")
class PackageInf(Base):
    def __init__(self,name="",version=[1,0,0],deps=[],hasBinary=True):
        self.name=name
        self.version=version
        self.deps=deps
        self.binary=hasBinary
def filterDeps(deps):
    d = copy(deps)
    p = loadPackageInfs()
    for item in p:
        if item in deps:
            deps.remove(item)
    return deps,d
def findDeps(dep):
    parents = []
    p = loadPackageInfs()
    for item in p.values():
        if dep in item["deps"]:
            parents.append(item["name"])
    return parents
def GeneratePackageInf(pkgInfs):
    z = {}
    for item in pkgInfs:
        x = pkgInfs[item]
        p = PackageInf(x["name"],x["version"],x["deps"],x["binary"])
        z[item] = p
    return z
def getDepList():
    deps = set()
    for item in GeneratePackageInf(loadPackageInfs()).values():
        for i in item.deps:
            deps.add(i)
    return deps
def loadPackageInfs():
    try:
        with open("config/pkginf.d","rb") as f:
            return pickle.load(f)
    except:
        with open("config/pkginf.d","wb") as f:
            pickle.dump({},f)
            return {}
def savePackageInfs(pkgInfs):
    with open("config/pkginf.d","wb") as f:
        pickle.dump(pkgInfs,f)
def registerPkgInf(pkgInf):
    pkgInfs = loadPackageInfs()
    pkgInfs[pkgInf["name"]] = pkgInf
    savePackageInfs(pkgInfs)
def downloadFile(url, fileName):
    urllib.request.urlretrieve(url, fileName)
    
def save_db(db):
    with open("config/pkm3.cfg","wb") as f:
        pickle.dump(db,f)
def list_app():
    z = []
    pkgs = loadPackageInfs()
    for pkg in pkgs:
        z.append(pkg)
    return sorted(z)
def update_db():
    DB = {
        "official":"https://github.com/WinFan3672/pkm_official/raw/main/pkm.db.cfg",
        "community":"https://github.com/WinFan3672/Pythinux/raw/main/Community/community.db.cfg",
        }
    try:
        with open("config/pkm3.cfg","rb") as f:
            return pickle.load(f)
    except:
        save_db(DB)
        return DB
def give_dbs(online=False,silent=False,fileName="config/db.pkm"):
    if not online:
        silent = True
    if not silent:
        print("Updating database...")
    dbs = update_db()
    db = {}
    if online:
        for item in dbs.keys():
            try:
                if not silent:
                    print(f"Downloading database '{item}'...")
                downloadFile(dbs[item],fileName)
                with open(fileName,"rb") as f:
                    x = pickle.load(f)
                db = mergeDict(db,x)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
            with open(fileName,"wb") as f:
                pickle.dump(db,f)
    else:
        try:
            with open(fileName,"rb") as f:
                return pickle.load(f)
        except:
            return give_dbs(True)
    if not silent:
        print("Successfully updated database.")
    return db
if args == ["version"] or args == ["-v"]:
    div()
    print("PKM {}".format(".".join([str(x) for x in VERSION])))
    div()
    print("PKM (c) 2023 WinFan3672, some rights reserved.")
    div()
elif args == ["update"]:
    if os.path.isfile("config/db.pkm"):
        os.remove("config/db.pkm")
    db = give_dbs(True)
elif "install" in args and len(args) >= 2:
    if "-y" in args:
        args.remove("-y")
        yesMode=True
    else:
        yesMode=False
    if "-d" in args:
        args.remove("-d")
        yesMode=True
        depMode=True
    else:
        depMode=False
    args.pop(0)
    for item in args:
        if not depMode:
            print(f"Installing {item}...")
        db = give_dbs(silent=True)
        print(f"Downloading package '{item}'...")
        if not item in db:
            div()
            print(f"Error: Cannot find package '{item}'")
        else:
            if db[item]["url"].startswith("link://"):
                x = db[item]["url"][7:]
                x = db[x]["url"]
            else:
                x = db[item]["url"]
            downloadFile(x,"tmp/pkm.szip3")
            if depMode:
                main(currentUser,"installd -d tmp/pkm.szip3",True)
            elif yesMode:
                main(currentUser,"installd -y tmp/pkm.szip3",True)
            else:
                main(currentUser,"installd tmp/pkm.szip3",True)
elif args == ["info"]:
    div()
    print("pkm info [package name]")
    div()
    print("Prints information about a package.")
    div()
elif "info" in args and len(args) == 2:
    args.remove("info")
    pkgs = loadPackageInfs()
    pkg = pkgs[args[0]]
    pkgDeps = pkg["deps"]
    depended = findDeps(args[0])
    depended = "; ".join(depended) if depended else "Nothing"
    div()
    print("Name: {}".format(pkg["humanName"]))
    print("Version: {}".format(".".join(pkg["version"])))
    print("Release Date: {}".format(pkg["releaseDate"]))
    print("Dependencies: {}".format("; ".join(pkgDeps) if pkgDeps else "None"))
    print("Required By: {}".format(depended))
    print("Package Type: {}".format('Binary' if bool(pkg["binary"]) else 'Library'))
    div()
elif args == ["db"]:
    div()
    print("pkm db [args]")
    div()
    print("Arguments:")
    print("    add: adds a database")
    print("    list: lists all databases")
    print("    remove: removes a database")
    print("    reset: reverts to the default")
    div()
elif args == ["db","add"]:
    div()
    print("pkm db add [db_name] [url]")
    div()
    print("Adds [url] to database list")
    div()
elif "db" in args and "add" in args and len(args) == 4:
    dbs = update_db()
    dbs[args[2]] = args[3]
    save_db(dbs)
elif args == ["db","remove"]:
    div()
    print("pkm db remove [database]")
    div()
    print("Removes [db] from database list.")
    div()
elif "remove" in args and len(args) == 2:
    d = getDepList()
    if args[1] in d:
        for item in findDeps(args[1]):
            print("ERROR: '{}' is a dependency of '{}' and cannot be removed.".format(args[1],item))
    else:
        p = loadPackageInfs()
        z = GeneratePackageInf(p)
        try:
            x = z[args[1]]
            if z[args[1]].binary:
                removeProgram(args[1])
            p.pop(args[1])
            savePackageInfs(p)
        except KeyError:
            print("ERROR: Invalid package name.")
elif "db" in args and "remove" in args and len(args) == 3:
    dbs = update_db()
    dbs.pop(args[2])
    save_db(dbs)
elif args == ["db","list"]:
    div()
    d = update_db()
    if d:
        for item in d.keys():
            print(f"{item} --> {d[item]}")
    else:
        print("Error: No databases.")
    div()
elif args == ["all"]:
    db = give_dbs(True)
    for item in db:
        div()
        print(item)
        div()
        print(db[item]["name"])
        print(db[item]["desc"])
    if db == {}:
        div()
        print("No packages found.")
    div()
elif args == ["allc"]:
    db = give_dbs(True,True)
    for item in db:
        print(item)
elif args == ["list"]:
    z = list_app()
    z= [z[i:i+10] for i in range(0, len(z), 10)]
    if z:
        div()
        for i in z:
            print(" ".join(i))
        div()
    else:
        div()
        print("No programs installed.")
        div()
elif args == ["install"]:
    div()
    print("pkm install [package]")
    div()
    print("Installs [package] if it is available.")
    div()
elif args == ["remove"]:
    div()
    print("pkm remove [package]")
    div()
    print("Removes [package].")
    div()
elif args == ["upgrade"]:
    i = 1
    z = list_app()
    pkgInfs = loadPackageInfs()
    x = []
    xdb = give_dbs(True)
    for item in z:
        if xdb[item]["version"] > pkgInfs[item]["version"]:
            x.append(item)
    if x:
        for item in x:
            print("({}/{}) Upgrading '{}'...".format(i,len(x),item))
            main(currentUser,f"pkm install -y {item}",True)
            i += 1
        print("All packages upgraded.")
    else:
        print("ERROR: No packages to upgrade.")
        print("Your system is fully up-to-date.")
elif "register" in args and len(args) == 7:
    if getTerm() == "installd":
        name = args[1]
        version = args[2]
        version = version.split(".")
        deps = args[3]
        hasBinary = bool(int(args[4]))
        humanName = args[5]
        releaseDate = args[6]
        if deps == "[]":
            deps = []
        else:
            deps = deps.split("|")
        c = {
            "name":name, 
            "version":version,
            "deps": deps,
            "binary":hasBinary,
            "humanName":humanName,
            "releaseDate":releaseDate,
            }
        registerPkgInf(c)
    else:
        print("Error: This is a hidden argument.")
        print("It is intended for use by internal programs only.")
        print("Trying to run it can break your system.")
elif args == ["clear"]:
    while list_app():
        for item in list_app():
            main(currentUser,"pkm remove {}".format(item))
    print("Successfully removed all programs.")
elif args == ["db","reset"]:
    os.remove("config/pkm3.cfg")
    update_db()
else:
    div()
    print("pkm [args]")
    div()
    print("PKM is Pythinux's package manager.")
    div()
    print("Positional arguments:")
    print("    install: installs a package")
    print("    remove: remove a package")
    print("    clear: removes all installed packages")
    print("    list: lists all installed programs")
    print("    info: prints information about an installed package")
    print("    all: lists all installable packages")
    print("    allc: lists all installable packages [compact]")
    print("    update: updates the database")
    print("    upgrade: upgrades all installed packages")
    print("    db: manages databases PKM accesses")
##    print("    batch: installs every package in a particular database")
    print("    version: states the version of PKM")
    div()
