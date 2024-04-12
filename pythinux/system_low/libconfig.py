import configparser

def load(filename, defaults={}):
    config = configparser.ConfigParser()
    for key in defaults.keys():
        config[key] = defaults[key]
    config.read(file.evalDir(filename, currentUser))
    save(config, filename) # Creates config if it doesn't exist
    return config

def save(config, filename):
    with open(file.evalDir(filename, currentUser), "w") as f:
        config.write(f)
