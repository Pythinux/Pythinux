import os
class Log:
    def __init__(self, filename, display=True):
        self.filename = filename
        self.logs = []
        self.display = display
        self.load()
    def log(self, text, log_type="info"):
        log_text = "[{}] {}".format(log_type, text)
        self.logs.append(log_text)
        if self.display:
            print(self.log_text)
        self.save()
    def load(self):
        if os.path.isfile(file.evalDir(self.filename, currentUser)):
            with file.open(self.filename, currentUser) as f:
                self.logs = f.read().split("\n")
    def save(self):
        with file.open(self.filename, currentUser, "w") as f:
            f.write("\n".join(self.logs))

