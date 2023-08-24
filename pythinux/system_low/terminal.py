def terminal(user):
    prompt = main(user,input(f"{user.group.name}@{user.username} $"))
    if prompt == LOGOFFEVENT:
        loginScreen()
    elif prompt in ["exit","quit"]:
        return
    elif prompt:
        if isinstance(prompt,list):
            div()
            if len(prompt) > 10:
                composite_list = [prompt[x:x+10] for x in range(0, len(prompt),10)]
                for item in composite_list:
                    print(" ".join(item))
            else:
                print(" ".join(prompt))
            div()
        else:
            print(prompt)
    terminal(user)
terminal(currentUser)
