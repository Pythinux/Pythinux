import getpass

def main(args):
    user = userList.byName(currentUser.username)
    user.password = hashString(getpass.getpass("[passwd] Enter your new password $"))
    saveUserList(userList)
    print("Successfully changed password.")

