# Getting Started
Getting started using Pythinux is simple. This is a user-friendly guide that tells you everything you need to know.
## Downloading
To download Pythinux, you have two options: a stable channel and and unstable channel.
### Unstable Channel
To download the latest unstable code, clone the GitHub repo. You will get the latest code, but it may have bugs that the latest stable release does not have.
### Stable Channel
To download the latest update, [navitage to the latest stable release](https://github.com/WinFan3672/Pythinux/releases/latest). Download the source code (ideally in zip format) and extract it. 
## Running
To run Pythinux, run the pythinux.py file in a modern version of python (3.9+).

``python pythinux.py``
## Setting Up
When you run Pythinux for the first time, the setup wizard will run. The setup wizard will:  
* Set up a root user for you
* Set up automatic login
## Using
Once the wizard completes, you will enter the main terminal, and it will look something like this:

```root@username $```

This is where you type commands.
## Useful Commands
There are a lof of commands in Pythinux, and understanding how to navigate Pythinux can be difficult.
### ``help``
This command lists every single command you can access. Every entry is split by a space (" ") and each line contains 10 programs.
### `man`
The `man` command is essentially a loader for built-in manuals. To load a manual, you type `man <manual name>`. For a list of manuals, `man /` provides a list of all of them. Some manuals are preinstalled, while others are installed by programs.
### `pkm`
This command is the official package manager for Pythinux. It has its own manpage ("man pkm") which details how to use it.
## Useful packages
There are a lot of packages in Pythinux. There are 2 repositories: `official` and `community`, both of which contain numerous packages you can install. 
The following packages may be of interest:  
* startpkg
	- Contains several packages from the official repository that may be of interest, such as a window manager and calculator, as well as some command-line utilities.
* pentools
	- Another collection of utilities. This collection contains a bunch of penetration testing utilities.