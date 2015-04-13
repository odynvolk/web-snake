# -*- coding: utf8 -*-

class ResultSet(object):
    def __init__(self):
        self.items = set()

    def put(self, obj):
        if type(obj) == list:
            self.items.update(obj)
        else:
            self.items.add(obj)

    def all(self):
        return self.items
