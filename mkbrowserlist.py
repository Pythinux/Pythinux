#!/usr/bin/python
import os
import markdown
page = "# Page List\nThis is an automatically generated page.\n\n"
for item in sorted(os.listdir("pages")):
    if item.endswith(".md"):
        item = item.replace(".md","")
        pagelet = "[about:{}](about:{})\n\n".format(item, item)
        page += pagelet
with open("pages/list.md","w") as f:
    f.write(page)
print("Successfully written about:list")