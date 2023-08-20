#!/usr/bin/python
import os
import pickle
import zipfile
db = {}
EXCLUSION_LIST = [".git"]
URL_BASE = "https://github.com/WinFan3672/Pythinux/raw/main/Community/"
print("Beginning build process.")
for item in os.listdir():
    if os.path.isdir(item) and item not in EXCLUSION_LIST:
        if "package.szip3" in os.listdir(item) and "program.info" in os.listdir(item):
            with open("{}/package.szip3".format(item),"rb") as f:
                with zipfile.ZipFile(f,"r") as zf:
                    with zf.open("program.info","r") as zff:
                        x = zff.readlines()[0].decode("utf-8")
                        x = x.split("|")
                        fileVersion = x[1].split(".")
            url = "{}{}/package.szip3".format(URL_BASE,item)
            with open(f"{item}/program.info") as f:
                g = f.read().split("|")
                if len(g) != 2:
                    print("ERROR: Invalid package info for {}.".format(item))
                    continue
            dic = {"name":g[0],
                "url":url,
                "desc":g[1],
                "version":fileVersion,
                }
            db[item] = dic
        else:
            print("ERROR: Package '{}' has missing files.".format(item))
with open("pkm.db.cfg","wb") as f:
    pickle.dump(db,f)
print("Build finished.")