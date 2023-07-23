import pickle

global db, dbs
db = {}
dbs = {}

import urllib.request
def downloadFile(url, fileName):
    if os.path.isfile(url):
        with open(url,"rb") as f:
            x=f.read()
        with open(fileName,"wb") as f:
            f.write(x)
    else:
        urllib.request.urlretrieve(url, fileName)
    
def save_db(db):
    with open("config/pkm3.cfg","wb") as f:
        pickle.dump(db,f)
def list_app():
    z = []
    dirs = ["app","app_high"]
    for d in dirs:
        x = os.listdir(d)
        for i in x:
            if i.endswith(".py"):
                z.append(i.replace(".py",""))
    return sorted(z)
def update_db():
    try:
        with open("config/pkm3.cfg","rb") as f:
            return pickle.load(f)
    except:
        save_db({"official":"https://winfan3672.000webhostapp.com/pkm3/pkm.db.cfg"})
        return {"official":"https://winfan3672.000webhostapp.com/pkm3/pkm.db.cfg"}
def give_dbs(online=False,silent=False,fileName="config/db.pkm"):
    if not online:
        silent = True
    if not silent:
        div()
        print("Updating database...")
        div()
    dbs = update_db()
    db = {}
    if online:
        for item in dbs.keys():
            try:
                if not silent:
                    print(f"Downloading Database '{item}'...")
                downloadFile(dbs[item],fileName)
                with open(fileName,"rb") as f:
                    x = pickle.load(f)
                db = mergeDict(db,x)
            except Exception as e:
                print(f"{type(e).__name__}: {e}")
    else:
        try:
            with open(fileName,"rb") as f:
                return pickle.load(f)
        except:
            print("No local copy, downloading fresh copy...")
            return give_dbs(True)
    if not silent:
        div()
        print("Successfully updated database.")
    return db
if args == ["version"] or args == ["-v"]:
    div()
    print("PKM 2.5.5")
    div()
    print("PKM (c) 2023 WinFan3672, some rights reserved.")
    div()
elif args == ["clear"]:
    for item in list_app():
        main(currentUser,f"pkm remove {item}")
elif args == ["update"]:
    give_dbs(True)
    div()
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
        if not item in db.keys():
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
                main(currentUser,"installd  tmp/pkm.szip3",True)
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
    main(currentUser,f"removed {args[1]}")
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
    div()
    for item in db:
        print(item)
    div()
elif args == ["list"]:
    z = list_app()
    x = []
    for i in z:
        x.append(i.replace(".py",""))
    z=x
    if z:
        div()
        print(" ".join(z))
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
    for item in z:
        print("({}/{}) Upgrading '{}'...".format(i,len(z),item))
        main(currentUser,f"pkm install -y {item}",True)
    print("All packages upgraded.")
elif args == ["db","reset"]:
    save_db({"official":"https://winfan3672.000webhostapp.com/pkm3/pkm.db.cfg"})
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
    print("    all: lists all installable packages")
    print("    allc: lists all installable packages [compact]")
    print("    update: updates the database")
    print("    upgrade: upgrades all installed packages")
    print("    db: manages databases PKM accesses")
##    print("    batch: installs every package in a particular database")
    print("    version: states the version of PKM")
    div()
