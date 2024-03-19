def main(args):
    if args == "-y":
        quit()
    else:
        if input("Enter 'quit' to confirm: ").lower() == "quit":
            quit()
        else:
            print("Action canceled.")
