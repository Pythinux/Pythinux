"""
libconfig: library for easy configuration file management using python's configparser module.

Code example:

libconfig = load_program("libconfig", currentUser, libMode=True)

## Make a default config
default = libconfig.newConfig()

## Set default values
default.add_section("settings")
default.set("settings", "allow_multiple_sessions", "false")
default.set("DEFAULT", "foo", "bar")

## Load the config

config = libconfig.loadConfig(default, os.path.expanduser("~/myapp.ini"))

## Get some values
print(config.getboolean("settings," "allow_multiple_sessions")) ## returns True
print(config.get("DEFAULT", "foo")) ## Returns 'bar'

## Save the config
libconfig.saveConfig(config, "~/myapp.ini")

For a full class reference: https://docs.python.org/3/library/configparser.html#configparser.ConfigParser

"""
import configparser
import copy

class Config(configparser.ConfigParser):
    """
    Copy of configparser.ConfigParser with a new copy() method.
    """
    def copy(self):
        return copy.deepcopy(self)

def saveConfig(config: Config, fileName: str):
    """
    Saves a Config to a file.
    """
    with open("config/{}.ini".format(fileName), "w") as f:
        config.write(f)

def newConfig(defaults={}):
    """
    Creates a new config file, with optional specified defaults.
    """
    return Config(defaults)

def loadConfig(default: Config, fileName: str):
    """
    Loads a config file and returns a Config.
    """
    config = default.copy()

    if os.path.isfile("config/{}.ini".format(fileName)):
        config.read([fileName])
    else:
        saveConfig(default, fileName)

    return config
