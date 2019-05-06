from Object import *

class Pickup(Object):
    def __init(self, objectSource):
        super().__init__()
        self.xpos = objectSource.xpos
        self.ypos = objectSource.ypos
        self.order = self.ypos
        self.typelist = ("health", "dynamite", "round", )
        self.type = self.typelist[0]
