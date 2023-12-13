class Registry:
    def __init__(self):
        self.registry = {}

    def create_key(self, path, *, exists_ok=False):
        if not path:
            raise ValueError("Path cannot be empty")

        components = path.split("\\")

        for i, component in enumerate(components):
            current_path = "\\".join(components[:i + 1])
            if current_path not in self.registry:
                self.registry[current_path] = {}

        if components[-1] in self.registry and not exists_ok:
            raise KeyError(f"Key '{path}' already exists")
        else:
            self.registry[components[-1]] = {}


    def delete_key(self, path):
        if path not in self.registry:
            raise KeyError(f"Key '{path}' doesn't exist")

        del self.registry[path]

    def get_entry(self, path, key):
        if path not in self.registry:
            raise KeyError(f"Key '{path}' doesn't exist")

        if key not in self.registry[path]:
            raise KeyError(f"Entry '{key}' doesn't exist in key '{path}'")

        return self.registry[path][key]

    def set_entry(self, path, key, value):
        if path not in self.registry:
            raise KeyError(f"Key '{path}' doesn't exist")

        self.registry[path][key] = value

    def delete_entry(self, path, key):
        if path not in self.registry:
            raise KeyError(f"Key '{path}' doesn't exist")

        if key not in self.registry[path]:
            raise KeyError(f"Entry '{key}' doesn't exist in key '{path}'")

        del self.registry[path][key]

    def get_all_entries(self, path):
        if path not in self.registry:
            raise KeyError(f"Key '{path}' doesn't exist")

        return self.registry[path].items()

reg = Registry()
reg.create_key("setting")
reg.create_key("setting.ui")
print(reg.registry) # {'setting': {}, 'setting/ui': {}}