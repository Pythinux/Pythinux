var = load_program("var", currentUser, libMode=True)

def main(args):
    if var.getbool("ALLOW_CLS", True):
        cls() 
