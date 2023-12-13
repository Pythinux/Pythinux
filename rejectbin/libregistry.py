import os
import pickle
default = {
    "setting": {},
    "assoc": {},
    "program": {},
    }
defaultUser = {
    "setting": {
        "shite":False,
        "more":"Shite",
        "count":0,
        "health":100.0,
        },
    }
def loadUserKey(registry):
    registry["user"] = defaultUser.copy()
    path = "home/{}/user_registry.pkl".format(currentUser.username)
    if os.path.isfile(path):
        with open(path, "rb") as f:
            registry["user"].update(pickle.load(f))
    else:
        with open(path, "wb") as f:
            pickle.dump(defaultUser, f)
def load_registry():
    registry = default.copy()
    if os.path.isfile("config/registry.pkl"):
        with open("config/registry.pkl","rb") as f:
            registry.update(pickle.load(f))
    else:
        with open("config/registry.pkl","wb") as f:
            pickle.dump(default, f)
    loadUserKey(registry)
    return registry

def saveUserKey(userKey):
    path = "home/{}/user_registry.pkl".format(currentUser.username)
    with open(path, "wb"):
        pickle.dump(userKey, f)
def saveRegistry(registry):
    reg = registry.copy()
    user = registry["user"].copy()
    reg.pop("user",None)
    with open("config/registry.pkl","wb") as f:
        pickle.dump(reg, f)
    saveUserKey(user)

def cleanDict(input_dict):
    allowed_key_types = (str)
    allowed_value_types = (int, float, bool, type(None), str, hex)

    filtered_dict = {}

    for key, value in input_dict.items():
        if isinstance(key, allowed_key_types) and isinstance(value, allowed_value_types):
            filtered_dict[key] = value
        elif isinstance(value, dict):
            nested_dict = cleanDict(value)
            if nested_dict:
                filtered_dict[key] = nested_dict

    return filtered_dict