import configparser

def load(filename, defaults={}, saveFile=True):
    config = configparser.ConfigParser()
    for key in defaults.keys():
        config[key] = defaults[key]
    config.read(file.evalDir(filename, currentUser))
    if saveFile:
        save(config, filename) # Creates config if it doesn't exist
    return config

def save(config, filename):
    with file.open(filename, currentUser, "w") as f:
        config.write(f)
