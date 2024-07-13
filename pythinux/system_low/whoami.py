def whoami(user):
    assertTrue(isinstance(user, User))
    return user.username
def main(args):
    print(whoami(currentUser))
