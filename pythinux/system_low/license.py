cls()
if os.path.isfile("../LICENSE"):
    with open("../LICENSE") as f:
        div()
        print(f.read())
        br()
else:
    print("ERROR: No license file found.")