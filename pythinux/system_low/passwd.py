import getpass

def main(args):
    if len(args) == 1 and currentUser.group.canSys:
        user = userList.byName(args[0])
    elif len(args) == 1:
        print("ERROR: Access denied.")
        return
    elif len(args) == 0:
        user = userList.byName(currentUser.username)
    else:
        print("ERROR: Invalid arguments.")
        return

    if not user.password == "" and not verifyHash("", user.password): 
        if not verifyHash(getpass.getpass("[passwd] Enter your current password $"), user.password):
            print("ERROR: Invalid password.")
            return

    user.password = hashString(getpass.getpass("[passwd] Enter your new password $"))
    saveUserList(userList)
    print("Successfully changed password.")
