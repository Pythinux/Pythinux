lst = sorted(list_loadable_programs(currentUser) + ['logoff'])
exclusions = desktopShell.getIconList(currentUser)
for item in exclusions:
    try:
        lst.remove(item["link"])
    except:
        pass
div()
print("Program List")
div()
if len(lst) >= 10:
     lst = [lst[i:i+10] for i in range(0, len(lst), 10)]
     for item in lst:
         print(" ".join(item))
else:
    print(" ".join(lst))
div()
