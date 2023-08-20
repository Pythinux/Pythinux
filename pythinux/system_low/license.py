cls()
if os.path.isfile("../helptopics/License"):
    with open("../helptopics/License") as f:
        div()
        print(f.read().replace("# ",""))
        div()
else:
    print("ERROR: No license file found.")    