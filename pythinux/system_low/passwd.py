import getpass
def main(args):
    userList = loadUserList()
    user = userList.byName(currentUser.username)
    passwd = hashString(getpass.getpass("[passwd] Enter your new password $"))
    user.password = passwd
    saveUserList(userList)
    print("Successfully changed password.")

