#!/usr/bin/python
import pythinux
class Permission:
    pass
class Storage:
    def __init__(self):
        self.read = Permission()
class permissions:
    def __init__(self):
        self.storage = Storage()
