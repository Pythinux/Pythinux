def whatami(user):
    assertTrue(isinstance(user, User))
    return user.group.name
def main(args):
    print(whatami(currentUser))
