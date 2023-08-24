class Point(Base):
    def __init__(self,text=None):
        self.text = text
    def execute(self):
        print(self.text)
class Div(Point):
    def execute(self):
        div()
class Break(Point):
    def execute(self):
        if self.text:
            input("Press ENTER to continue.")
        else:
            br()
class Clear(Point):
    def execute(self):
        cls()
class NETerminal(Point):
    def execute(self):
        prompt = ""
        while prompt != self.text:
            prompt = input("[TUTORIAL] {}@{} $".format(currentUser.group.name,currentUser.username))
            if prompt == "":
                continue
            elif prompt != self.text:
                print("ERROR: Invalid command.")
                print("HINT: You're supposed to type '{}'.".format(self.text))
        print("ERROR: The tutorial does not allow you to execute that command.")
class Terminal(Point):
    def execute(self):
        prompt = ""
        while prompt != self.text:
            prompt = input("[TUTORIAL] {}@{} $".format(currentUser.group.name,currentUser.username))
            if prompt == "":
                continue
            elif prompt != self.text:
                print("ERROR: Invalid command.")
                print("HINT: You're supposed to type '{}'.".format(self.text))
        main(currentUser,self.text)
if args == ["5"]:
    points = [
        Clear(),
        Div(),
        Point("This is the final part of the tutorial."),
        Point("It explains how to get help on almost anything, if you ever become stuck."),
        Break(),
        Clear(),
        Div(),
        Point("For a list of commands, type `help`."),
        Point("Commands with arguments will have help information if you don't provide any arguments, so just run them."),
        Point("The `man` command will help you if a program has a manpage."),
        Point("If you need to view a program's source code, the `xview` package (included with startpkg) can help."),
        Point("Worst case scenario, you can go to the GitHub, read through the documentation, and if you're still stuck, create an Issue."),
        Break(),
        Clear(),
        Div(),
        Point("You have finished the tutorial."),
        Break(),
        Clear(),
        ]
elif args == ["4"]:
    points = [
        Clear(),
        Point("Now that you're installed and removed some packages, let's examine them further."),
        Point("pkm info is used to do this."),
        Point("Use said command on the xutil package."),
        Terminal("pkm info xutil"),
        Point("pkm info only works on installed packages."),
        Point("It shows the dependency tree of the package as well as other info."),
        Point("You can see what a package depends on and what packages depend on it."),
        Break(),
        Clear(),
        Break(),
        Point("If you want a list of packages you can install, `pkm all` is your friend."),
        Point("Continue by testing it out."),
        Break(),
        Clear(),
        Terminal("pkm all"),
        Break(),
        Clear(),
        Point("The `pkm all` command lists all packages as well as their full names and descriptions."),
        Point("A more compact version (pkm allc) simply lists every installable packages."),
        Terminal("pkm allc"),
        Break(),
        Clear(),
        Point("The next part of the tutorial can be accessed using `tutorial 5`."),
        Break(),
        Clear(),
        ]
elif args == ["3"]:
    points = [
        Clear(),
        Div(),
        Point("Welcome back."),
        Point("Installing and managing packages is simple."),
        Point("The pkm command is your friend in that regard."),
        Break(),
        Clear(),
        Point("Try running it."),
        Terminal("pkm"),
        Point("As you can see, it can be a bit complex."),
        Point("However, we will break it down command by command."),
        Break(),
        Clear(),
        Div(),
        Point("PKM internally caches a database of packages and their URL's."),
        Point("It sometimes updates it automatically, but it doesn't do so when installing packages."),
        Break(),
        Clear(),
        Point("To manually update it, run `pkm update`."),
        Terminal("pkm update"),
        Point("It updated the database so that new packages are registered."),
        Point("Now to install a package."),
        Break(),
        Clear(),
        Div(),
        Point("Installing packages is simple."),
        Point("You run pkm install <package name>."),
        Break(),
        Clear(),
        Point("Install the `xutil` package."),
        Terminal("pkm install xutil"),
        Point("The xutil package has several dependencies."),
        Point("You cannot remove a package if it is a dependency."),
        Break(),
        Clear(),
        Point("Try to remove the xcount package."),
        Terminal("pkm remove xcount"),
        Point("Oh no, it's locked by xutil. Remove that."),
        Terminal("pkm remove xutil"),
        Point("And again."),
        NETerminal("pkm remove startpkg"),
        Point("Dependency protection is useful to prevent breaking programs."),
        Point("To continue the tutorial, run `tutorial 4`."),
        Break(),
        Clear(),
        ]      
elif args == ["2"]:
    points = [
        Clear(),
        Div(),
        Point("Welcome back to the tutorial."),
        Point("This part of the tutorial focuses on packages."),
        Break(),
        Clear(),
        Div(),
        Point("Now that you have installed argtest, we might as well use it to demonstrate a point."),
        Point("Pythinux separates arguments by spaces."),
        Point("This may have undesirable effects."),
        Point("Try it by running `argtest hello world`."),
        Terminal("argtest hello world"),
        Point("You can see that `hello` and `world` are two different packages."),
        Point("Now do the same, but surround `hello world` with apostrophes."),
        Terminal("argtest 'hello world'"),
        Point("The two arguments become one, as desired."),
        Point("You may need to keep this in mind when using progams."),
        Break(),
        Clear(),
        Div(),
        Point("Moving away from arguments from a second, this next part is about manuals."),
        Point("If you've used linux, I'm sure you're familiar with manpages."),
        Point("They're instruction manuals that certain commands have which are opened with the `man` command."),
        Point("Turns out, Pythinux has them as well."),
        Break(),
        Clear(),
        Point("Run the man command for instructions."),
        Terminal("man"),
        Point("Based on what the command showed, get `man` to show a list of commands."),
        Terminal("man /"),
        Point("Now, load the `initd` manuals."),
        Terminal("man initd"),
        Break(),
        Clear(),
        Div(),
        Point("The next part of the tutorial can be loaded by running the following command:"),
        Point("tutorial 3"),
        Break(),
        Clear(),
        ]
else:
    points = [
        Clear(),
        Div(),
        Point("Welcome to the Pythinux tutorial."),
        Point("This is an interactive utility providing a brief overview on how to use Pythinux."),
        Point("There will be points where you will need to interact with the system."),
        Point("This will occur in a somewhat controlled environment."),
        Point("You may require an Internet connection to run some commands."),
        Break(),
        Clear(),
        Div(),
        Point("The first thing to understand is the terminal. It looks something like this:"),
        Div(),
        Point("{}@{} $".format(currentUser.group.name,currentUser.username)),
        Div(),
        Point("The dollar sign marks the end of the prompt, and is where you type."),
        Point("The first word is the name of the group the user is currently in."),
        Point("The @ is a separator."),
        Point("The last one is your username."),
        Break(),
        Clear(),
        Div(),
        Point("The first command you need to understand is `help`."),
        Point("It lists every single command you can execute."),
        Point("Try it out using the interactive prompt."),
        Break(),
        Clear(),
        Terminal("help"),
        Point("As you can see, when you ran the command, the actual command executed in the shell."),
        Point("The tutorial will follow a similar formula."),
        Point("You will type a command, and it will run, so that you understand how it works."),
        Break(),
        Clear(),
        Point("Your next task is to execute the `about` command."),
        Terminal("about"),
        Point("You ran the about command, and it shows about information."),
        Point("The next part of the tutorial is about command arguments."),
        Break(),
        Clear(),
        Div(),
        Point("The command-line actually supports arguments."),
        Point("These get passed to the command once you run it."),
        Point("Many commands do not parse arguments, and will ignore them."),
        Point("However, some do."),
        Point("An example is `echo`, which will print whatever you pass to it."),
        Break(),
        Clear(),
        Point("Try it out."),
        Point("Run `echo hello world` and see what happens."),
        Terminal("echo hello world"),
        Div(),
        Point("As you can see, the command saw your argument and passed it."),
        Break(),
        Clear(),
        Div(),
        Point("However, there is a slightly annoying thing about arguments, which is that they are separated by spaces."),
        Point("This means that more advanced programs, which take multiple arguments, break if you add spaces into an argument."),
        Point("This is the system treats the argument as multiple ones, and the command fails."),
        Point("In the case of `echo`, it simply merges the arguments together, but more complex programs don't do this."),
        Point("In order to truncate multiple arguments into a single one, you need to surround it in apostrophes (')."),
        Break(),
        Clear(),
        Div(),
        Point("A good way of demonstrating this is using a program you can install using pkm."),
        Point("`pkm` is the package manager for Pythinux."),
        Point("It's very complex, but its user-facing functionality is pretty simple."),
        Break(),
        Clear(),
        Point("As an example, let's install a package we need."),
        Point("Using pkm, install the `argtest` package."),
        Terminal("pkm install argtest"),
        Break(),
        Clear(),
        Div(),
        Point("The next part of the tutorial can be started by running:"),
        Point("tutorial 2"),
        Point("If the installation of `argtest` failed for some reason,"),
        Point("Make sure that it is installed before continuing."),
        Break(),
    ]
for point in points:
    point.execute()