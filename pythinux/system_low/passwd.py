import getpass

def main(args):
    user = userList.byName(currentUser.username)
    if not verifyHash("", user.password) and not verifyHash(getpass.getpass("[passwd] Enter your current password $"), user.password):
        print("ERROR: Invalid password.")
        return
    user.password = hashString(getpass.getpass("[passwd] Enter your new password $"))
    saveUserList(userList)
    print("Successfully changed password.")
