import getpass

def main(args):
    userList = loadUserList()
    user = userList.byName(currentUser.username)
    user.passwd = hashString(getpass.getpass("[passwd] Enter your new password $"))
    saveUserList(userList)
    print("Successfully changed password.")

