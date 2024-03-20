"""
libconfig2: library for easy configuration file management using python's configparser module.

Code example:

libconfig = load_program("libconfig2", currentUser, libMode=True)

## Load a config
default = libconfig.newConfig({"foo": "bar", "isEnabled": True})
config = libconfig.loadConfig(default, os.path.expanduser("~/myapp.ini"))

## Retrieve a value

print(config.get("foo")) ## Prints 'bar'
print(config.getbool("isEnabled")) ## Prints "True"

## Modify the config
config.set("bar", "foo")

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

    if os.path.isfile(fileName):
        config.read([filename])
    else:
        saveConfig(default, fileName)

    return config

def main(args):
    pass
